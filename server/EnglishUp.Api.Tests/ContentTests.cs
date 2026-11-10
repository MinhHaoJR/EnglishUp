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

        Assert.Empty((await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);
        Assert.Equal(HttpStatusCode.Forbidden,
            (await learner.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);
        Assert.Equal(HttpStatusCode.Unauthorized,
            (await anonymous.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);

        Assert.Equal(HttpStatusCode.OK,
            (await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") })).StatusCode);
        var item = Assert.Single((await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);
        Assert.Equal(("word", "a-1", false), (item.Kind, item.Id, item.Hidden));
        Assert.Equal("harbour", item.Data!.Value.GetProperty("word").GetString());

        // Saving again edits the same row.
        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1", "port") });
        item = Assert.Single((await anonymous.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);
        Assert.Equal("port", item.Data!.Value.GetProperty("word").GetString());
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
    public async Task Hide_ThenDelete_RestoresTheBundledItem()
    {
        using var factory = new ApiFactory();
        var admin = await AdminTests.Learner(factory, admin: true);

        // Hiding a bundled item needs no data; the row is a tombstone.
        Assert.Equal(HttpStatusCode.OK,
            (await admin.PostAsJsonAsync("/api/admin/content/reading/r-1/hide", new { hidden = true })).StatusCode);
        var item = Assert.Single((await admin.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);
        Assert.True(item.Hidden);
        Assert.Null(item.Data);

        // Showing it again leaves no empty row behind.
        Assert.Equal(HttpStatusCode.NoContent,
            (await admin.PostAsJsonAsync("/api/admin/content/reading/r-1/hide", new { hidden = false })).StatusCode);
        Assert.Empty((await admin.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);

        // An edited item keeps its edit when hidden and shown again.
        await admin.PutAsJsonAsync("/api/admin/content/word/a-1", new { data = Word("a-1") });
        await admin.PostAsJsonAsync("/api/admin/content/word/a-1/hide", new { hidden = true });
        await admin.PostAsJsonAsync("/api/admin/content/word/a-1/hide", new { hidden = false });
        Assert.False(Assert.Single((await admin.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!).Hidden);

        await admin.PostAsJsonAsync("/api/admin/content/reading/r-1/hide", new { hidden = true });
        Assert.Equal(HttpStatusCode.NoContent, (await admin.DeleteAsync("/api/admin/content/reading/r-1")).StatusCode);
        await admin.DeleteAsync("/api/admin/content/word/a-1");
        Assert.Empty((await admin.GetFromJsonAsync<List<ContentItemDto>>("/api/content"))!);
        Assert.Equal(HttpStatusCode.NotFound, (await admin.DeleteAsync("/api/admin/content/reading/r-1")).StatusCode);
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
