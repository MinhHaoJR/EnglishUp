using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;

namespace EnglishUp.Api.Tests;

public class SyncTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private record Tokens(string AccessToken);

    private async Task<HttpClient> SignedInClient()
    {
        var client = factory.CreateClient();
        var credentials = new { email = $"sync-{Guid.NewGuid():N}@example.test", password = "Learn#2026" };
        (await client.PostAsJsonAsync("/api/register", credentials)).EnsureSuccessStatusCode();
        var tokens = await (await client.PostAsJsonAsync("/api/login", credentials)).Content.ReadFromJsonAsync<Tokens>();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", tokens!.AccessToken);
        return client;
    }

    private static object Attempt(string id, double score = 80) =>
        new { id, skill = "reading", score, duration = 60, timestamp = 1000, label = "Passage 1" };

    private static object Review(double lastReviewed) =>
        new { store = "reviews", id = "w1", version = lastReviewed, data = new { id = "w1", lastReviewed } };

    private static async Task<SyncPayload> Sync(HttpClient client, object[] attempts, object[] records)
    {
        var response = await client.PostAsJsonAsync("/api/sync", new { attempts, records });
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        return (await response.Content.ReadFromJsonAsync<SyncPayload>())!;
    }

    [Fact]
    public async Task Sync_RequiresToken()
    {
        var response = await factory.CreateClient()
            .PostAsJsonAsync("/api/sync", new { attempts = Array.Empty<object>(), records = Array.Empty<object>() });
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task TwoDevices_MergeAttemptsAndKeepNewestRecord()
    {
        var client = await SignedInClient();
        await Sync(client, [Attempt("a1")], [Review(500)]);

        // A second device sends a retry of a1, a new attempt and an older copy of the review.
        var merged = await Sync(client, [Attempt("a1", score: 10), Attempt("a2")], [Review(300)]);
        Assert.Equal(["a1", "a2"], merged.Attempts.Select(a => a.Id).Order());
        Assert.Equal(80, merged.Attempts.Single(a => a.Id == "a1").Score);
        var review = Assert.Single(merged.Records);
        Assert.Equal(500, review.Version);
        Assert.Equal(500, review.Data.GetProperty("lastReviewed").GetDouble());

        var newer = await Sync(client, [], [Review(900)]);
        Assert.Equal(900, Assert.Single(newer.Records).Data.GetProperty("lastReviewed").GetDouble());
        Assert.Equal(2, newer.Attempts.Count);
    }

    [Fact]
    public async Task Accounts_AreIsolated()
    {
        await Sync(await SignedInClient(), [Attempt("shared-id")], [Review(500)]);

        var other = await Sync(await SignedInClient(), [Attempt("shared-id", score: 20)], []);
        Assert.Equal(20, Assert.Single(other.Attempts).Score);
        Assert.Empty(other.Records);
    }

    [Fact]
    public async Task OptionalLanguage_IsOmittedNotNull()
    {
        var client = await SignedInClient();
        var response = await client.PostAsJsonAsync("/api/sync", new { attempts = new[] { Attempt("a1") }, records = Array.Empty<object>() });
        using var json = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.False(json.RootElement.GetProperty("attempts")[0].TryGetProperty("learningLanguage", out _));
    }

    [Theory]
    [InlineData("""{ "attempts": [{ "id": "a", "skill": "reading", "score": 150, "duration": 1, "timestamp": 1, "label": "x" }], "records": [] }""")]
    [InlineData("""{ "attempts": [{ "id": "a", "skill": "cooking", "score": 50, "duration": 1, "timestamp": 1, "label": "x" }], "records": [] }""")]
    [InlineData("""{ "attempts": [], "records": [{ "store": "secrets", "id": "x", "version": 1, "data": {} }] }""")]
    [InlineData("""{ "attempts": [], "records": [{ "store": "drafts", "id": "", "version": 1, "data": {} }] }""")]
    [InlineData("""{ "attempts": [], "records": [{ "store": "drafts", "id": "d", "version": 1, "data": "text" }] }""")]
    [InlineData("""{ "records": [] }""")]
    public async Task InvalidPayload_IsRejectedWithoutSaving(string body)
    {
        var client = await SignedInClient();
        var response = await client.PostAsync("/api/sync", new StringContent(body, System.Text.Encoding.UTF8, "application/json"));
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var state = await Sync(client, [], []);
        Assert.Empty(state.Attempts);
        Assert.Empty(state.Records);
    }
}
