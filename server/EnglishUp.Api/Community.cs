using System.Security.Claims;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record ProfileDto(string DisplayName, bool ShowOnLeaderboard);

public record AchievementDto(string Code, int Points, DateTimeOffset? EarnedAt);

public record LeaderboardEntry(int Rank, string DisplayName, int Points, bool IsMe);

public record LeaderboardDto(string Period, List<LeaderboardEntry> Entries, int MyPoints, bool MyRowShown);

/// <summary>Learner profiles, achievements and the leaderboard.</summary>
public static class Community
{
    private const int LeaderboardSize = 50;

    /// <summary>Badge rules live here; their bilingual names live in the client.</summary>
    private record Rule(string Code, int Points, Func<Facts, bool> Earned);

    private record Facts(int Attempts, int PerfectAttempts, int Skills, int LongestStreak, int ReviewedWords);

    private static readonly Rule[] Rules =
    [
        new("first-practice", 10, f => f.Attempts >= 1),
        new("streak-3", 20, f => f.LongestStreak >= 3),
        new("streak-7", 50, f => f.LongestStreak >= 7),
        new("all-skills", 30, f => f.Skills >= 5),
        new("perfect-10", 30, f => f.PerfectAttempts >= 10),
        new("words-100", 50, f => f.ReviewedWords >= 100),
    ];

    public static int Bonus(string code) => Rules.Single(r => r.Code == code).Points;

    public static void MapCommunity(this IEndpointRouteBuilder api)
    {
        api.MapGet("/profile", async (ClaimsPrincipal user, AppDbContext db) =>
        {
            var profile = await ProfileAsync(db, UserId(user));
            await db.SaveChangesAsync();
            return Results.Ok(new ProfileDto(profile.DisplayName, profile.ShowOnLeaderboard));
        }).RequireAuthorization();

        api.MapPut("/profile", async (ProfileDto input, ClaimsPrincipal user, AppDbContext db) =>
        {
            var name = input.DisplayName?.Trim() ?? "";
            if (name.Length is < 2 or > 40 || name.Any(char.IsControl))
                return Results.ValidationProblem(new Dictionary<string, string[]>
                {
                    ["displayName"] = ["Display name must be 2–40 printable characters."],
                });
            var profile = await ProfileAsync(db, UserId(user));
            profile.DisplayName = name;
            profile.ShowOnLeaderboard = input.ShowOnLeaderboard;
            await db.SaveChangesAsync();
            return Results.Ok(new ProfileDto(profile.DisplayName, profile.ShowOnLeaderboard));
        }).RequireAuthorization();

        api.MapGet("/achievements", async (ClaimsPrincipal user, AppDbContext db) =>
        {
            var userId = UserId(user);
            var earned = await db.UserAchievements.Where(a => a.UserId == userId)
                .ToDictionaryAsync(a => a.Code, a => a.EarnedAt);
            return Results.Ok(Rules.Select(r =>
                new AchievementDto(r.Code, r.Points, earned.TryGetValue(r.Code, out var at) ? at : null)));
        }).RequireAuthorization();

        api.MapGet("/leaderboard", async (string? period, ClaimsPrincipal user, AppDbContext db) =>
        {
            if (period is not (null or "week" or "all")) return Results.BadRequest();
            var userId = UserId(user);
            var ledger = db.PointLedger.AsQueryable();
            if (period != "all")
            {
                var today = Points.Today(DateTimeOffset.UtcNow);
                var monday = today.AddDays(-(((int)today.DayOfWeek + 6) % 7));
                ledger = ledger.Where(p => p.LocalDate >= monday);
            }

            var top = await ledger
                .Join(db.LearnerProfiles.Where(p => p.ShowOnLeaderboard), l => l.UserId, p => p.UserId,
                    (l, p) => new { l.UserId, p.DisplayName, l.Points })
                .GroupBy(x => new { x.UserId, x.DisplayName })
                .Select(g => new { g.Key.UserId, g.Key.DisplayName, Points = g.Sum(x => x.Points) })
                .OrderByDescending(x => x.Points).ThenBy(x => x.DisplayName)
                .Take(LeaderboardSize)
                .ToListAsync();
            var shown = await db.LearnerProfiles.AnyAsync(p => p.UserId == userId && p.ShowOnLeaderboard);
            var mine = await ledger.Where(p => p.UserId == userId).SumAsync(p => p.Points);

            return Results.Ok(new LeaderboardDto(
                period ?? "week",
                top.Select((x, i) => new LeaderboardEntry(i + 1, x.DisplayName, x.Points, x.UserId == userId)).ToList(),
                mine,
                shown));
        }).RequireAuthorization();
    }

    /// <summary>Returns the learner's profile, adding a hidden default one on first use.</summary>
    public static async Task<LearnerProfile> ProfileAsync(AppDbContext db, string userId)
    {
        var profile = await db.LearnerProfiles.FindAsync(userId);
        if (profile is not null) return profile;
        profile = new LearnerProfile
        {
            UserId = userId,
            DisplayName = $"Học viên {Random.Shared.Next(1000, 10000)}",
            CreatedAt = DateTimeOffset.UtcNow,
        };
        db.LearnerProfiles.Add(profile);
        return profile;
    }

    /// <summary>Awards badges whose rules now hold, with their bonus points. Call after attempts are saved.</summary>
    public static async Task AwardAchievementsAsync(AppDbContext db, string userId, DateTimeOffset now)
    {
        var earned = await db.UserAchievements.Where(a => a.UserId == userId).Select(a => a.Code).ToListAsync();
        if (earned.Count == Rules.Length) return;

        var attempts = await db.Attempts.Where(a => a.UserId == userId)
            .Select(a => new { a.Skill, a.Score, a.Timestamp }).ToListAsync();
        var days = attempts
            .Select(a => Points.Today(DateTimeOffset.FromUnixTimeMilliseconds((long)a.Timestamp)))
            .Distinct().Order().ToList();
        var facts = new Facts(
            attempts.Count,
            attempts.Count(a => a.Score >= 100),
            attempts.Select(a => a.Skill).Distinct().Count(),
            LongestRun(days),
            await db.SyncRecords.CountAsync(r => r.UserId == userId && r.Store == "reviews"));

        var today = Points.Today(now);
        foreach (var rule in Rules.Where(r => !earned.Contains(r.Code) && r.Earned(facts)))
        {
            db.UserAchievements.Add(new UserAchievement { UserId = userId, Code = rule.Code, EarnedAt = now });
            db.PointLedger.Add(new PointEntry
            {
                UserId = userId, Source = "achievement", SourceId = rule.Code,
                Points = rule.Points, LocalDate = today, CreatedAt = now,
            });
        }
    }

    /// <summary>Longest run of consecutive calendar days in a sorted, distinct list.</summary>
    public static int LongestRun(IReadOnlyList<DateOnly> days)
    {
        int best = 0, run = 0;
        for (var i = 0; i < days.Count; i++)
        {
            run = i > 0 && days[i].DayNumber == days[i - 1].DayNumber + 1 ? run + 1 : 1;
            best = Math.Max(best, run);
        }
        return best;
    }

    private static string UserId(ClaimsPrincipal user) => user.FindFirstValue(ClaimTypes.NameIdentifier)!;
}
