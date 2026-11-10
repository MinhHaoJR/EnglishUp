using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

/// <summary>
/// Demo classmates so the leaderboard and badges are not empty in a presentation. They have no password (nobody can
/// sign in as them), their names end in "(demo)", and <see cref="RemoveAsync"/> deletes them with every row they own.
/// </summary>
public static class Demo
{
    public const string EmailDomain = "demo.englishup.invalid";
    private static readonly string[] Names = ["Minh Anh", "Gia Huy", "Bảo Ngọc", "Đức Thịnh", "Thu Hà", "Quang Khải"];
    private static readonly string[] Skills = ["vocabulary", "listening", "speaking", "reading", "writing", "grammar"];

    /// <summary>Replaces any earlier demo learners with fresh ones whose history ends today.</summary>
    public static async Task<int> SeedAsync(AppDbContext db, UserManager<IdentityUser> users, DateTimeOffset now)
    {
        await RemoveAsync(db);
        var random = new Random(2026); // the same leaderboard on every run
        var ids = new List<string>();
        for (var n = 0; n < Names.Length; n++)
        {
            var email = $"demo-{n + 1}@{EmailDomain}";
            var user = new IdentityUser { UserName = email, Email = email, EmailConfirmed = true };
            var created = await users.CreateAsync(user);
            if (!created.Succeeded)
                throw new InvalidOperationException(string.Join("; ", created.Errors.Select(e => e.Description)));
            ids.Add(user.Id);
            db.LearnerProfiles.Add(new LearnerProfile
            {
                UserId = user.Id, DisplayName = $"{Names[n]} (demo)", ShowOnLeaderboard = true, CreatedAt = now,
            });

            // The first learner practised every day for two weeks, each next one for two days fewer.
            for (var day = 13 - n * 2; day >= 0; day--)
            {
                for (var k = random.Next(2, 6); k > 0; k--)
                {
                    var at = now.AddDays(-day).AddMinutes(-20 * k);
                    var score = random.Next(40, 101);
                    var id = $"demo-{n + 1}-{day}-{k}";
                    db.Attempts.Add(new Attempt
                    {
                        UserId = user.Id, Id = id, Skill = Skills[random.Next(Skills.Length)], Score = score,
                        Duration = random.Next(60, 600), Timestamp = at.ToUnixTimeMilliseconds(), Label = "Demo practice",
                    });
                    // At most 5 attempts of 5 points a day, far below the daily cap.
                    db.PointLedger.Add(new PointEntry
                    {
                        UserId = user.Id, Source = "attempt", SourceId = id, Points = Points.ForAttempt(score),
                        LocalDate = Points.Today(at), CreatedAt = at,
                    });
                }
            }
        }
        await db.SaveChangesAsync();
        foreach (var id in ids) await Community.AwardAchievementsAsync(db, id, now);
        await db.SaveChangesAsync();
        return ids.Count;
    }

    /// <summary>Deletes the demo learners and their rows; returns how many learners were removed.</summary>
    public static async Task<int> RemoveAsync(AppDbContext db)
    {
        var ids = await db.Users.Where(u => u.Email!.EndsWith("@" + EmailDomain)).Select(u => u.Id).ToListAsync();
        if (ids.Count == 0) return 0;
        // PostgreSQL would cascade these; deleting them here keeps the in-memory test database consistent too.
        db.Attempts.RemoveRange(db.Attempts.Where(a => ids.Contains(a.UserId)));
        db.PointLedger.RemoveRange(db.PointLedger.Where(p => ids.Contains(p.UserId)));
        db.UserAchievements.RemoveRange(db.UserAchievements.Where(a => ids.Contains(a.UserId)));
        db.LearnerProfiles.RemoveRange(db.LearnerProfiles.Where(p => ids.Contains(p.UserId)));
        db.Users.RemoveRange(db.Users.Where(u => ids.Contains(u.Id)));
        await db.SaveChangesAsync();
        return ids.Count;
    }
}
