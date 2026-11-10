using System.Net.Http.Json;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

public class DemoTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private async Task<T> With<T>(Func<AppDbContext, UserManager<IdentityUser>, Task<T>> action)
    {
        using var scope = factory.Services.CreateScope();
        return await action(scope.ServiceProvider.GetRequiredService<AppDbContext>(),
            scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>());
    }

    [Fact]
    public async Task Seed_FillsTheLeaderboard_RunsAgainWithoutDuplicates_AndRemovesCleanly()
    {
        var client = await factory.SignedInClient();
        var now = DateTimeOffset.UtcNow;

        Assert.Equal(6, await With((db, users) => Demo.SeedAsync(db, users, now)));
        Assert.Equal(6, await With((db, users) => Demo.SeedAsync(db, users, now)));

        var board = (await client.GetFromJsonAsync<LeaderboardDto>("/api/leaderboard?period=all"))!;
        var demo = board.Entries.Where(e => e.DisplayName.EndsWith("(demo)")).ToList();
        Assert.Equal(6, demo.Count);
        Assert.Equal("Minh Anh (demo)", demo[0].DisplayName); // practised the most days
        Assert.All(demo, e => Assert.True(e.Points > 0));

        var badges = await With((db, _) => db.UserAchievements
            .Join(db.LearnerProfiles, a => a.UserId, p => p.UserId, (a, p) => new { a.Code, p.DisplayName })
            .Where(x => x.DisplayName == "Minh Anh (demo)").Select(x => x.Code).ToListAsync());
        Assert.Contains("streak-7", badges);

        Assert.Equal(6, await With((db, _) => Demo.RemoveAsync(db)));
        board = (await client.GetFromJsonAsync<LeaderboardDto>("/api/leaderboard?period=all"))!;
        Assert.DoesNotContain(board.Entries, e => e.DisplayName.EndsWith("(demo)"));
        Assert.Equal(0, await With((db, _) => db.Attempts.CountAsync(a => a.Label == "Demo practice")));
        Assert.Equal(0, await With((db, _) => Demo.RemoveAsync(db)));
    }
}
