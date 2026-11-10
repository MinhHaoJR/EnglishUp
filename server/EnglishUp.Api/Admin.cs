using System.Security.Claims;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record MeDto(string Email, bool IsAdmin);
public record OverviewDto(
    int Users, int Online, int Offline, int ActiveToday, int Locked, int Admins,
    int AttemptsToday, int QuestionsToday, int GamesToday, int KnowledgeChunks,
    int OnlineWindowSeconds, DateTimeOffset At);
public record AdminUserDto(
    string Id, string Email, string? DisplayName, bool ShowOnLeaderboard, bool IsAdmin, bool Locked,
    DateTimeOffset? LastSeenAt, bool Online, int Points, int Attempts);
public record LockRequest(bool Locked);

/// <summary>
/// Presence (who has the app open) and the admin area. Learners' clients send a heartbeat every
/// minute while the app is open; anyone seen within <see cref="OnlineWindow"/> counts as online.
/// Admins are Identity users in the "Admin" role, granted with `dotnet run -- admin &lt;email&gt;`.
/// </summary>
public static class Admin
{
    public const string Role = "Admin";
    public const string Policy = "Admin";
    public static readonly TimeSpan OnlineWindow = TimeSpan.FromMinutes(2);
    private const int MaxUsers = 500;

    /// <summary>Puts an existing account in the Admin role; false when no account has that email.</summary>
    public static async Task<bool> GrantAsync(UserManager<IdentityUser> users, RoleManager<IdentityRole> roles, string email)
    {
        var user = await users.FindByEmailAsync(email.Trim());
        if (user is null) return false;
        if (!await roles.RoleExistsAsync(Role)) await roles.CreateAsync(new IdentityRole(Role));
        if (!await users.IsInRoleAsync(user, Role)) await users.AddToRoleAsync(user, Role);
        return true;
    }

    /// <summary>Takes an account out of the Admin role; false when no account has that email.</summary>
    public static async Task<bool> RevokeAsync(UserManager<IdentityUser> users, string email)
    {
        var user = await users.FindByEmailAsync(email.Trim());
        if (user is null) return false;
        if (await users.IsInRoleAsync(user, Role)) await users.RemoveFromRoleAsync(user, Role);
        // A new stamp ends the account's refresh token, so the role leaves its next token too.
        await users.UpdateSecurityStampAsync(user);
        return true;
    }

    public static void MapAdmin(this IEndpointRouteBuilder api)
    {
        api.MapPost("/presence", async (ClaimsPrincipal user, AppDbContext db, TimeProvider clock) =>
        {
            var userId = UserId(user);
            var presence = await db.Presence.FindAsync(userId);
            if (presence is null) db.Presence.Add(new Presence { UserId = userId, LastSeenAt = clock.GetUtcNow() });
            else presence.LastSeenAt = clock.GetUtcNow();
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                // Two tabs sent their first heartbeat at once; the other one recorded the visit.
            }
            return Results.NoContent();
        }).RequireAuthorization();

        api.MapGet("/me", async (ClaimsPrincipal user, UserManager<IdentityUser> users) =>
        {
            var account = await users.GetUserAsync(user);
            return account is null
                ? Results.Unauthorized()
                : Results.Ok(new MeDto(account.Email ?? "", await users.IsInRoleAsync(account, Role)));
        }).RequireAuthorization();

        var admin = api.MapGroup("/admin").RequireAuthorization(Policy);

        admin.MapGet("/overview", async (AppDbContext db, TimeProvider clock) =>
        {
            var now = clock.GetUtcNow();
            var since = now - OnlineWindow;
            var today = Points.StartOfToday(now);
            var todayMs = today.ToUnixTimeMilliseconds();
            var users = await db.Users.CountAsync();
            var online = await db.Presence.CountAsync(p => p.LastSeenAt >= since);
            var roleId = await db.Roles.Where(r => r.Name == Role).Select(r => r.Id).FirstOrDefaultAsync();
            return Results.Ok(new OverviewDto(
                users,
                online,
                users - online,
                await db.Presence.CountAsync(p => p.LastSeenAt >= today),
                await db.Users.CountAsync(u => u.LockoutEnd != null && u.LockoutEnd > now),
                roleId is null ? 0 : await db.UserRoles.CountAsync(r => r.RoleId == roleId),
                await db.Attempts.CountAsync(a => a.Timestamp >= todayMs),
                await db.ChatMessages.CountAsync(m => m.Role == "user" && m.CreatedAt >= today),
                await db.GameSessions.CountAsync(g => g.StartedAt >= today),
                await db.KnowledgeChunks.CountAsync(),
                (int)OnlineWindow.TotalSeconds,
                now));
        });

        admin.MapGet("/users", async (string? search, AppDbContext db, TimeProvider clock) =>
        {
            var now = clock.GetUtcNow();
            var since = now - OnlineWindow;
            var query = db.Users.AsQueryable();
            if (!string.IsNullOrWhiteSpace(search))
            {
                var term = search.Trim().ToUpperInvariant();
                var named = db.LearnerProfiles.Where(p => p.DisplayName.ToUpper().Contains(term)).Select(p => p.UserId);
                query = query.Where(u => u.NormalizedEmail!.Contains(term) || named.Contains(u.Id));
            }
            var accounts = await query.OrderBy(u => u.Email).Take(MaxUsers)
                .Select(u => new { u.Id, u.Email, u.LockoutEnd }).ToListAsync();
            var ids = accounts.Select(a => a.Id).ToList();

            var profiles = await db.LearnerProfiles.Where(p => ids.Contains(p.UserId))
                .ToDictionaryAsync(p => p.UserId);
            var seen = await db.Presence.Where(p => ids.Contains(p.UserId))
                .ToDictionaryAsync(p => p.UserId, p => p.LastSeenAt);
            var points = await db.PointLedger.Where(p => ids.Contains(p.UserId)).GroupBy(p => p.UserId)
                .Select(g => new { g.Key, Sum = g.Sum(p => p.Points) }).ToDictionaryAsync(x => x.Key, x => x.Sum);
            var attempts = await db.Attempts.Where(a => ids.Contains(a.UserId)).GroupBy(a => a.UserId)
                .Select(g => new { g.Key, Count = g.Count() }).ToDictionaryAsync(x => x.Key, x => x.Count);
            var roleId = await db.Roles.Where(r => r.Name == Role).Select(r => r.Id).FirstOrDefaultAsync();
            var admins = (await db.UserRoles.Where(r => r.RoleId == roleId && ids.Contains(r.UserId))
                .Select(r => r.UserId).ToListAsync()).ToHashSet();

            return Results.Ok(accounts
                .Select(a =>
                {
                    profiles.TryGetValue(a.Id, out var profile);
                    DateTimeOffset? last = seen.TryGetValue(a.Id, out var at) ? at : null;
                    return new AdminUserDto(
                        a.Id, a.Email ?? "", profile?.DisplayName, profile?.ShowOnLeaderboard ?? false,
                        admins.Contains(a.Id), a.LockoutEnd > now, last, last >= since,
                        points.GetValueOrDefault(a.Id), attempts.GetValueOrDefault(a.Id));
                })
                // The spine of the admin page: most recently seen first, never-seen last.
                .OrderByDescending(u => u.LastSeenAt ?? DateTimeOffset.MinValue).ThenBy(u => u.Email)
                .ToList());
        });

        admin.MapPost("/users/{id}/lock", async (string id, LockRequest input, ClaimsPrincipal user,
            UserManager<IdentityUser> users) =>
        {
            if (id == UserId(user))
                return Results.ValidationProblem(new Dictionary<string, string[]>
                {
                    ["id"] = ["Admins cannot lock their own account."],
                });
            var account = await users.FindByIdAsync(id);
            if (account is null) return Results.NotFound();
            await users.SetLockoutEnabledAsync(account, true);
            await users.SetLockoutEndDateAsync(account, input.Locked ? DateTimeOffset.MaxValue : null);
            // A new stamp makes the account's refresh token useless, so a locked learner is out within the hour.
            if (input.Locked) await users.UpdateSecurityStampAsync(account);
            return Results.NoContent();
        });

        admin.MapPost("/users/{id}/hide", async (string id, AppDbContext db) =>
        {
            var profile = await db.LearnerProfiles.FindAsync(id);
            if (profile is null) return Results.NotFound();
            profile.ShowOnLeaderboard = false;
            await db.SaveChangesAsync();
            return Results.NoContent();
        });
    }

    private static string UserId(ClaimsPrincipal user) => user.FindFirstValue(ClaimTypes.NameIdentifier)!;
}
