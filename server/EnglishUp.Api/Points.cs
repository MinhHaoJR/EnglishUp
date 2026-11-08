using System.Security.Claims;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record PointsDto(int Total, int Today, int DailyCap);

/// <summary>Server-side scoring: the client never sends points, only attempts.</summary>
public static class Points
{
    public const int DailyCap = 300;
    private static readonly TimeSpan MaxAttemptAge = TimeSpan.FromDays(7);
    // shortcut: every learner uses Vietnam time; add a TimeZone column to LearnerProfiles if learners abroad join.
    private static readonly TimeZoneInfo Zone = TimeZoneInfo.FindSystemTimeZoneById("Asia/Ho_Chi_Minh");

    /// <summary>1 point for trying, up to 5 for a perfect score.</summary>
    public static int ForAttempt(double score) => 1 + (int)Math.Floor(Math.Clamp(score, 0, 100) / 25);

    public static DateOnly Today(DateTimeOffset now) =>
        DateOnly.FromDateTime(TimeZoneInfo.ConvertTime(now, Zone).DateTime);

    /// <summary>
    /// Adds ledger rows for attempts saved for the first time in this request. Attempts older than
    /// seven days (an imported backup) are kept without points, and practice never exceeds the daily cap
    /// (badge bonuses do not count towards it).
    /// </summary>
    public static async Task AwardAsync(AppDbContext db, string userId, IEnumerable<Attempt> added, DateTimeOffset now)
    {
        var today = Today(now);
        var remaining = await RemainingTodayAsync(db, userId, today);
        var cutoff = (now - MaxAttemptAge).ToUnixTimeMilliseconds();
        foreach (var attempt in added.Where(a => a.Timestamp >= cutoff).OrderBy(a => a.Timestamp))
        {
            var points = Math.Min(ForAttempt(attempt.Score), remaining);
            if (points <= 0) break;
            db.PointLedger.Add(new PointEntry
            {
                UserId = userId, Source = "attempt", SourceId = attempt.Id,
                Points = points, LocalDate = today, CreatedAt = now,
            });
            remaining -= points;
        }
    }

    /// <summary>Practice and game points still available today; badge bonuses do not use the cap.</summary>
    public static async Task<int> RemainingTodayAsync(AppDbContext db, string userId, DateOnly today) =>
        DailyCap - await db.PointLedger
            .Where(p => p.UserId == userId && p.LocalDate == today && p.Source != "achievement")
            .SumAsync(p => p.Points);

    public static void MapPoints(this IEndpointRouteBuilder api) =>
        api.MapGet("/points", async (ClaimsPrincipal user, AppDbContext db) =>
        {
            var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;
            var today = Today(DateTimeOffset.UtcNow);
            var mine = db.PointLedger.Where(p => p.UserId == userId);
            return Results.Ok(new PointsDto(
                await mine.SumAsync(p => p.Points),
                await mine.Where(p => p.LocalDate == today).SumAsync(p => p.Points),
                DailyCap));
        }).RequireAuthorization();
}
