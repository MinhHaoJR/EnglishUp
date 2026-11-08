using System.Net;
using System.Net.Http.Json;

namespace EnglishUp.Api.Tests;

public class PointsTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private static readonly double Now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();

    private static object Attempt(string id, double score, double timestamp) =>
        new { id, skill = "vocabulary", score, duration = 5, timestamp, label = "word" };

    private static async Task Sync(HttpClient client, IEnumerable<object> attempts) =>
        (await client.PostAsJsonAsync("/api/sync", new { attempts, records = Array.Empty<object>() }))
        .EnsureSuccessStatusCode();

    private static async Task<PointsDto> Points(HttpClient client) =>
        (await client.GetFromJsonAsync<PointsDto>("/api/points"))!;

    [Theory]
    [InlineData(0, 1)]
    [InlineData(24, 1)]
    [InlineData(25, 2)]
    [InlineData(80, 4)]
    [InlineData(100, 5)]
    public void AttemptPoints_RiseWithScore(double score, int points) =>
        Assert.Equal(points, EnglishUp.Api.Points.ForAttempt(score));

    [Fact]
    public async Task Points_RequireToken()
    {
        var response = await factory.CreateClient().GetAsync("/api/points");
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task NewAttempts_EarnPointsOnlyOnce()
    {
        var client = await factory.SignedInClient();
        object[] attempts = [Attempt("a1", 100, Now), Attempt("a2", 30, Now), Attempt("a3", 0, Now)];

        await Sync(client, attempts);
        await Sync(client, attempts);

        var points = await Points(client);
        Assert.Equal(5 + 2 + 1, points.Today);
        Assert.Equal(points.Today, points.Total);
        Assert.Equal(300, points.DailyCap);
    }

    [Fact]
    public async Task DailyCap_StopsFurtherPoints()
    {
        var client = await factory.SignedInClient();
        await Sync(client, Enumerable.Range(0, 70).Select(i => Attempt($"a{i}", 100, Now + i)));

        Assert.Equal(300, (await Points(client)).Today);
    }

    [Fact]
    public async Task AttemptsOlderThanAWeek_AreKeptWithoutPoints()
    {
        var client = await factory.SignedInClient();
        var eightDaysAgo = Now - TimeSpan.FromDays(8).TotalMilliseconds;
        await Sync(client, [Attempt("old", 100, eightDaysAgo)]);

        Assert.Equal(0, (await Points(client)).Total);
        var state = await (await client.PostAsJsonAsync("/api/sync", new { attempts = Array.Empty<object>(), records = Array.Empty<object>() }))
            .Content.ReadFromJsonAsync<SyncPayload>();
        Assert.Single(state!.Attempts);
    }

    [Fact]
    public async Task Points_BelongToTheirLearner()
    {
        var first = await factory.SignedInClient();
        await Sync(first, [Attempt("a1", 100, Now)]);

        Assert.Equal(0, (await Points(await factory.SignedInClient())).Total);
    }
}
