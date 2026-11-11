using System.Net;
using System.Net.Http.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

public class ContentTests
{
    private static object Word(string id, string word = "harbour") => new
    {
        id, word, ipa = "/ˈhɑːbə/", pos = "noun", meaning = "bến cảng", definition = "a sheltered place for boats",
        examples = new[] { "The boats wait in the harbour." }, level = "B1", topic = "travel",
    };

    [Fact]
    public async Task Content_IsPublicToRead_AndOnlyAdminsChangeIt()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        var learner = await AdminTests.Learner(factory);
        var anonymous = factory.CreateClient();

        var seeded = (await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!;
        Assert.Equal(Content.ReadSeed(Content.SeedFolder).Count, seeded.Count);
        Assert.Equal(HttpStatusCode.Forbidden,
            (await learner.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);
        Assert.Equal(HttpStatusCode.Unauthorized,
            (await anonymous.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);

        Assert.Equal(HttpStatusCode.OK,
            (await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);
        var words = (await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!.Where(i => i.Kind == "word").ToList();
        // A new item goes last in its kind.
        Assert.Equal(("a-1", false), (words[^1].Id, words[^1].Hidden));
        Assert.Equal("harbour", words[^1].Data.GetProperty("word").GetString());

        // Saving again edits the same row.
        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1", "port") });
        var all = (await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!;
        Assert.Equal(seeded.Count + 1, all.Count);
        Assert.Equal("port", all.Single(i => i.Id == "a-1").Data.GetProperty("word").GetString());
    }

    [Theory]
    [InlineData("poem", "a-1")] // unknown kind
    [InlineData("word", "bad id!")] // id format
    [InlineData("word", "a-2")] // data.id differs from the address
    public async Task Save_RejectsBadEnvelopes(string kind, string id)
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        var response = await admin.PutAsJsonAsync($"/api/admin/content/{Uri.EscapeDataString(kind)}/{Uri.EscapeDataString(id)}",
            new { data = Word("a-1") });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task Save_RequiresEachKindsFields()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        var response = await admin.PutAsJsonAsync("/api/admin/content/word/a-1",
            new { data = new { id = "a-1", word = "harbour", meaning = " " } });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        var body = await response.Content.ReadAsStringAsync();
        Assert.Contains("data.meaning", body);
        Assert.Contains("data.examples", body);
    }

    [Fact]
    public async Task Hide_Show_AndDelete()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        async Task<ContentItemDto?> Get(string id) =>
            (await admin.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!.SingleOrDefault(i => i.Id == id);

        Assert.Equal(HttpStatusCode.OK,
            (await admin.PostAsJsonAsync("/api/admin/content/reading/r1/hide", new { hidden = true })).StatusCode);
        Assert.True((await Get("r1"))!.Hidden);
        await admin.PostAsJsonAsync("/api/admin/content/reading/r1/hide", new { hidden = false });
        Assert.False((await Get("r1"))!.Hidden);

        Assert.Equal(HttpStatusCode.NoContent, (await admin.DeleteAsync("/api/admin/content/reading/r1")).StatusCode);
        Assert.Null(await Get("r1"));
        Assert.Equal(HttpStatusCode.NotFound, (await admin.DeleteAsync("/api/admin/content/reading/r1")).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound,
            (await admin.PostAsJsonAsync("/api/admin/content/reading/r1/hide", new { hidden = true })).StatusCode);
    }

    [Fact]
    public async Task Content_RevalidatesWithItsETag()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        var anonymous = factory.CreateClient();
        var first = await anonymous.GetAsync("/api/content");
        var etag = first.Headers.ETag!;

        var again = new HttpRequestMessage(HttpMethod.Get, "/api/content");
        again.Headers.IfNoneMatch.Add(etag);
        Assert.Equal(HttpStatusCode.NotModified, (await anonymous.SendAsync(again)).StatusCode);

        // A change gives a new version, so browsers download it.
        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") });
        var changed = new HttpRequestMessage(HttpMethod.Get, "/api/content");
        changed.Headers.IfNoneMatch.Add(etag);
        Assert.Equal(HttpStatusCode.OK, (await anonymous.SendAsync(changed)).StatusCode);
    }

    [Fact]
    public async Task OnlyTheLibraryIsCompressed()
    {
        using var factory = new ApiFactory();
        var client = factory.CreateClient();
        HttpRequestMessage Gzip(string path)
        {
            var request = new HttpRequestMessage(HttpMethod.Get, path);
            request.Headers.AcceptEncoding.ParseAdd("gzip");
            return request;
        }

        var library = await client.SendAsync(Gzip("/api/content"));
        Assert.Contains("gzip", library.Content.Headers.ContentEncoding);
        // Signed-in responses carry tokens and personal data, so they are never compressed.
        var learner = await AdminTests.Learner(factory);
        var leaderboard = await learner.SendAsync(Gzip("/api/leaderboard"));
        Assert.Equal(HttpStatusCode.OK, leaderboard.StatusCode);
        Assert.Empty(leaderboard.Content.Headers.ContentEncoding);
    }

    [Fact]
    public async Task Seed_KeepsAdminEdits_UnlessOverwritten()
    {
        using var factory = new ApiFactory();
        using var scope = factory.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var seed = Content.ReadSeed(Content.SeedFolder);
        Assert.Equal(2491, seed.Count(r => r.Kind == "word"));
        Assert.Equal(Content.SeedFiles.Count, seed.Select(r => r.Kind).Distinct().Count());

        var word = await db.ContentItems.SingleAsync(c => c.Kind == "word" && c.Id == seed[0].Id);
        word.Json = word.Json.Insert(1, "\"note\":\"edited\",");
        db.ContentItems.Remove(await db.ContentItems.SingleAsync(c => c.Kind == "reading" && c.Id == "r1"));
        await db.SaveChangesAsync();

        Assert.Equal(new SeedReport(1, 0, seed.Count - 1), await Content.SeedAsync(db, Content.SeedFolder, DateTimeOffset.UtcNow));
        Assert.Contains("edited", (await db.ContentItems.AsNoTracking().SingleAsync(c => c.Id == seed[0].Id && c.Kind == "word")).Json);

        Assert.Equal(new SeedReport(0, 1, seed.Count - 1),
            await Content.SeedAsync(db, Content.SeedFolder, DateTimeOffset.UtcNow, overwrite: true));
        Assert.DoesNotContain("edited", (await db.ContentItems.AsNoTracking().SingleAsync(c => c.Id == seed[0].Id && c.Kind == "word")).Json);
    }

    [Fact]
    public async Task AdminChanges_ReachTheAssistantAtOnce()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);
        async Task<KnowledgeChunk?> Chunk()
        {
            using var scope = factory.Services.CreateScope();
            return await scope.ServiceProvider.GetRequiredService<AppDbContext>().KnowledgeChunks
                .SingleOrDefaultAsync(c => c.SourceType == "word" && c.SourceId == "a-1");
        }

        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") });
        Assert.Contains("bến cảng", (await Chunk())!.Text);
        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1", "port") });
        Assert.Equal("port", (await Chunk())!.Title);

        await admin.PostAsJsonAsync("/api/admin/content/word/a-1/hide", new { hidden = true });
        Assert.Null(await Chunk());
        await admin.PostAsJsonAsync("/api/admin/content/word/a-1/hide", new { hidden = false });
        Assert.NotNull(await Chunk());
        await admin.DeleteAsync("/api/admin/content/word/a-1");
        Assert.Null(await Chunk());
    }
}
