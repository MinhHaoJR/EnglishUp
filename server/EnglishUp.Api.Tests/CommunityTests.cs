using System.Net;
using System.Net.Http.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

public class CommunityTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private static readonly double Now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
    private const double Day = 86_400_000;

    private static object Attempt(string id, string skill = "reading", double score = 80, double? timestamp = null) =>
        new { id, skill, score, duration = 30, timestamp = timestamp ?? Now, label = "x" };

    private static async Task Sync(HttpClient client, IEnumerable<object> attempts, IEnumerable<object>? records = null) =>
        (await client.PostAsJsonAsync("/api/sync", new { attempts, records = records ?? [] })).EnsureSuccessStatusCode();

    private static async Task<HttpClient> Named(HttpClient client, string name, bool shown = true)
    {
        (await client.PutAsJsonAsync("/api/profile", new { displayName = name, showOnLeaderboard = shown }))
            .EnsureSuccessStatusCode();
        return client;
    }

    private static async Task<LeaderboardDto> Board(HttpClient client, string period = "week") =>
        (await client.GetFromJsonAsync<LeaderboardDto>($"/api/leaderboard?period={period}"))!;

    private static async Task<Dictionary<string, DateTimeOffset?>> Badges(HttpClient client) =>
        (await client.GetFromJsonAsync<List<AchievementDto>>("/api/achievements"))!.ToDictionary(a => a.Code, a => a.EarnedAt);

    [Theory]
    [InlineData("/api/profile")]
    [InlineData("/api/achievements")]
    [InlineData("/api/leaderboard")]
    public async Task Endpoints_RequireToken(string path) =>
        Assert.Equal(HttpStatusCode.Unauthorized, (await factory.CreateClient().GetAsync(path)).StatusCode);

    [Fact]
    public async Task NewProfile_IsHiddenWithAGeneratedName()
    {
        var profile = await (await factory.SignedInClient()).GetFromJsonAsync<ProfileDto>("/api/profile");
        Assert.StartsWith("Học viên ", profile!.DisplayName);
        Assert.False(profile.ShowOnLeaderboard);
    }

    [Theory]
    [InlineData("")]
    [InlineData(" a ")]
    [InlineData("bad\u0007name")]
    [InlineData("12345678901234567890123456789012345678901")]
    public async Task Profile_RejectsInvalidNames(string name)
    {
        var response = await (await factory.SignedInClient())
            .PutAsJsonAsync("/api/profile", new { displayName = name, showOnLeaderboard = true });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task Profile_SavesTrimmedName()
    {
        var client = await Named(await factory.SignedInClient(), "  Minh Hào  ");
        var profile = await client.GetFromJsonAsync<ProfileDto>("/api/profile");
        Assert.Equal(new ProfileDto("Minh Hào", true), profile);
    }

    [Fact]
    public async Task Leaderboard_ListsOnlyOptedInLearnersByPoints()
    {
        var first = await Named(await factory.SignedInClient(), $"First {Guid.NewGuid():N}"[..20]);
        var second = await Named(await factory.SignedInClient(), $"Second {Guid.NewGuid():N}"[..20]);
        var hidden = await Named(await factory.SignedInClient(), $"Hidden {Guid.NewGuid():N}"[..20], shown: false);
        await Sync(first, [Attempt("a1", score: 100), Attempt("a2", score: 100)]);
        await Sync(second, [Attempt("b1", score: 0)]);
        await Sync(hidden, [Attempt("c1", score: 100), Attempt("c2", score: 100), Attempt("c3", score: 100)]);

        var seenByHidden = await Board(hidden);
        var names = seenByHidden.Entries.Select(e => e.DisplayName).ToList();
        Assert.True(names.FindIndex(n => n.StartsWith("First")) < names.FindIndex(n => n.StartsWith("Second")));
        Assert.DoesNotContain(names, n => n.StartsWith("Hidden"));
        Assert.False(seenByHidden.MyRowShown);
        Assert.Equal(3 * 5 + Community.Bonus("first-practice"), seenByHidden.MyPoints);

        var seenByFirst = await Board(first);
        var me = Assert.Single(seenByFirst.Entries, e => e.IsMe);
        Assert.Equal(2 * 5 + Community.Bonus("first-practice"), me.Points);
        Assert.True(seenByFirst.MyRowShown);
    }

    [Fact]
    public async Task WeeklyLeaderboard_LeavesOutOlderPoints()
    {
        var client = await Named(await factory.SignedInClient(), "Weekly learner");
        await Sync(client, [Attempt("w1", score: 100)]);
        using (var scope = factory.Services.CreateScope())
        {
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var userId = await db.LearnerProfiles.Where(p => p.DisplayName == "Weekly learner").Select(p => p.UserId).SingleAsync();
            db.PointLedger.Add(new PointEntry
            {
                UserId = userId, Source = "attempt", SourceId = "old", Points = 100,
                LocalDate = Points.Today(DateTimeOffset.UtcNow).AddDays(-14), CreatedAt = DateTimeOffset.UtcNow,
            });
            await db.SaveChangesAsync();
        }

        var thisWeek = 5 + Community.Bonus("first-practice");
        Assert.Equal(thisWeek, (await Board(client, "week")).MyPoints);
        Assert.Equal(thisWeek + 100, (await Board(client, "all")).MyPoints);
    }

    [Fact]
    public async Task Leaderboard_RejectsUnknownPeriod()
    {
        var response = await (await factory.SignedInClient()).GetAsync("/api/leaderboard?period=year");
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task Badges_AreEarnedOnceFromSyncedHistory()
    {
        var client = await factory.SignedInClient();
        Assert.All(await Badges(client), b => Assert.Null(b.Value));

        await Sync(client, [
            Attempt("d1", "reading", timestamp: Now - 2 * Day),
            Attempt("d2", "listening", timestamp: Now - Day),
            Attempt("d3", "speaking"),
            Attempt("d4", "writing"),
            Attempt("d5", "vocabulary"),
        ]);
        var badges = await Badges(client);
        Assert.NotNull(badges["first-practice"]);
        Assert.NotNull(badges["all-skills"]);
        Assert.NotNull(badges["streak-3"]);
        Assert.Null(badges["streak-7"]);
        Assert.Null(badges["words-100"]);

        var reviews = Enumerable.Range(0, 100)
            .Select(i => new { store = "reviews", id = $"w{i}", version = Now, data = new { id = $"w{i}" } });
        await Sync(client, [], reviews);
        Assert.NotNull((await Badges(client))["words-100"]);

        var points = await client.GetFromJsonAsync<PointsDto>("/api/points");
        var bonuses = new[] { "first-practice", "all-skills", "streak-3", "words-100" }.Sum(Community.Bonus);
        Assert.Equal(5 * Points.ForAttempt(80) + bonuses, points!.Total);
    }

    [Theory]
    [InlineData(new int[0], 0)]
    [InlineData(new[] { 1 }, 1)]
    [InlineData(new[] { 1, 2, 3, 5, 6 }, 3)]
    [InlineData(new[] { 1, 3, 4, 5, 6, 8 }, 4)]
    public void LongestRun_CountsConsecutiveDays(int[] offsets, int expected)
    {
        var start = new DateOnly(2026, 12, 30);
        Assert.Equal(expected, Community.LongestRun(offsets.Select(d => start.AddDays(d)).ToList()));
    }
}
