using System.Net;
using System.Net.Http.Json;
using System.Text.RegularExpressions;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

/// <summary>Bag-of-words vectors: texts sharing words point the same way, so ranking is predictable offline.</summary>
public class FakeEmbedder : IEmbedder
{
    private const int Size = 4096;
    public string Model { get; set; } = "fake-embedding";
    public int Calls { get; private set; }
    public HttpStatusCode? Failure { get; set; }

    /// <summary>Document calls that fail with 429 before one succeeds.</summary>
    public int RateLimited { get; set; }
    public bool DailyQuota { get; set; }

    public Task<float[][]> EmbedDocumentsAsync(IReadOnlyList<ChunkSource> chunks, CancellationToken ct = default)
    {
        Calls++;
        if (DailyQuota) throw new DailyQuotaException();
        if (RateLimited-- > 0) throw new HttpRequestException("fake", null, HttpStatusCode.TooManyRequests);
        return Task.FromResult(chunks.Select(c => Vector(c.Title + " " + c.Text)).ToArray());
    }

    public Task<float[]> EmbedQueryAsync(string query, CancellationToken ct = default)
    {
        Calls++;
        if (Failure is { } status) throw new HttpRequestException("fake", null, status);
        return Task.FromResult(Vector(query));
    }

    private static float[] Vector(string text)
    {
        var vector = new float[Size];
        foreach (Match word in Regex.Matches(text.ToLowerInvariant(), "[a-z]+"))
        {
            // FNV-1a: string.GetHashCode changes per run, which would make rankings flaky.
            var hash = 2166136261u;
            foreach (var ch in word.Value) hash = (hash ^ ch) * 16777619u;
            vector[hash % Size]++;
        }
        return vector;
    }
}

public class KnowledgeTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private static readonly string Content = Path.Combine(AppContext.BaseDirectory, "Content");

    private static AppDbContext NewDb() =>
        new(new DbContextOptionsBuilder<AppDbContext>().UseInMemoryDatabase(Guid.NewGuid().ToString()).Options);

    [Fact]
    public void BuildChunks_CoversEveryContentFileOnce()
    {
        var chunks = Knowledge.BuildChunks(EnglishUp.Api.Content.ReadSeed(Content));
        var counts = chunks.GroupBy(c => c.SourceType).ToDictionary(g => g.Key, g => g.Count());
        Assert.Equal(2430, counts["word"]);
        Assert.Equal(6, counts["reading"]);
        Assert.Equal(6, counts["listening"]);
        Assert.Equal(10, counts["writing"]);
        Assert.Equal(100, counts["grammar"]);
        Assert.Equal(chunks.Count, chunks.Select(c => (c.SourceType, c.SourceId)).Distinct().Count());
        Assert.All(chunks, c => Assert.True(c.Title.Length <= 200 && c.Text.Length <= 4000, c.SourceId));
        var routine = chunks.Single(c => c is { SourceType: "word", Title: "routine" });
        Assert.Contains("Vietnamese meaning:", routine.Text);
    }

    [Fact]
    public void BuildChunks_SkipsHiddenBrokenAndPracticeRows()
    {
        var chunks = Knowledge.BuildChunks([
            new ContentItem { Kind = "word", Id = "a-new", Position = 1, Json = """
                {"id":"a-new","word":"harbour","ipa":"","pos":"noun","meaning":"bến cảng","definition":"a place for boats",
                 "examples":["Boats wait in the harbour."],"level":"B1","topic":"travel"}
                """ },
            new ContentItem { Kind = "structure", Id = "s1", Json = """
                {"id":"s1","group":"x","formula":"S + V","meaning":"m","example":"e","key":"k","options":["a","b"],"translation":"t"}
                """ },
            new ContentItem { Kind = "reading", Id = "r-hidden", Hidden = true, Json = """{"id":"r-hidden","title":"t","level":"A1","topic":"x","text":"y"}""" },
            new ContentItem { Kind = "word", Id = "a-broken", Json = """{"id":"a-broken"}""" },
            new ContentItem { Kind = "word", Id = "a-other", Json = """{"id":"another","word":"w","meaning":"m","examples":[]}""" },
            new ContentItem { Kind = "speaking", Id = "a-talk", Json = """{"id":"a-talk","title":"Talk"}""" },
        ]);

        // Patterns come before words, so lessons are embedded first.
        Assert.Equal(["s1", "a-new"], chunks.Select(c => c.SourceId));
        Assert.Contains("bến cảng", chunks[1].Text);
    }

    [Fact]
    public async Task Ingest_EmbedsOnlyNewOrChangedChunks()
    {
        using var db = NewDb();
        var embedder = new FakeEmbedder();
        List<ChunkSource> sources =
        [
            new("word", "1", "apple", "a fruit"), new("word", "2", "book", "pages to read"),
            new("reading", "r1", "Morning", "Linh walks to the park."),
        ];
        Assert.Equal(new IngestReport(3, 0, 0, 0), await Knowledge.IngestAsync(db, embedder, sources, batchSize: 2));
        Assert.Equal(2, embedder.Calls);

        Assert.Equal(new IngestReport(0, 0, 3, 0), await Knowledge.IngestAsync(db, embedder, sources));
        Assert.Equal(2, embedder.Calls);

        sources = [sources[0] with { Text = "a red fruit" }, sources[2]];
        Assert.Equal(new IngestReport(0, 1, 1, 1), await Knowledge.IngestAsync(db, embedder, sources));
        Assert.Equal("a red fruit", (await db.KnowledgeChunks.SingleAsync(c => c.SourceId == "1")).Text);

        sources = [.. sources, new("word", "3", "cat", "a pet"), new("word", "4", "dog", "another pet")];
        Assert.Equal(new IngestReport(1, 0, 2, 0, 1), await Knowledge.IngestAsync(db, embedder, sources, max: 1));
        Assert.Equal(new IngestReport(1, 0, 3, 0), await Knowledge.IngestAsync(db, embedder, sources));
        sources = sources[..2];
        await Knowledge.IngestAsync(db, embedder, sources);

        embedder.Model = "fake-embedding-v2";
        Assert.Equal(new IngestReport(0, 2, 0, 0), await Knowledge.IngestAsync(db, embedder, sources));
        Assert.All(await db.KnowledgeChunks.ToListAsync(), c => Assert.Equal("fake-embedding-v2", c.EmbeddingModel));
    }

    [Fact]
    public async Task Ingest_WaitsOutRateLimitsButStopsAfterMaxTries()
    {
        using var db = NewDb();
        List<ChunkSource> sources = [new("word", "1", "apple", "a fruit")];
        var embedder = new FakeEmbedder { RateLimited = 2 };
        Assert.Equal(1, (await Knowledge.IngestAsync(db, embedder, sources, retryAfter: TimeSpan.Zero)).Added);
        Assert.Equal(3, embedder.Calls);

        embedder = new FakeEmbedder { RateLimited = Gemini.MaxTries };
        sources = [new("word", "2", "book", "pages")];
        await Assert.ThrowsAsync<HttpRequestException>(() =>
            Knowledge.IngestAsync(db, embedder, sources, retryAfter: TimeSpan.Zero));
        Assert.Equal(Gemini.MaxTries, embedder.Calls);

        embedder = new FakeEmbedder { DailyQuota = true };
        await Assert.ThrowsAsync<DailyQuotaException>(() =>
            Knowledge.IngestAsync(db, embedder, sources, retryAfter: TimeSpan.FromHours(1)));
        Assert.Equal(1, embedder.Calls);
    }

    [Fact]
    public async Task Search_RequiresTokenAndValidInput()
    {
        Assert.Equal(HttpStatusCode.Unauthorized,
            (await factory.CreateClient().GetAsync("/api/knowledge/search?q=routine")).StatusCode);
        var client = await factory.SignedInClient();
        foreach (var query in new[] { "q=", "q=%20%20", $"q={new string('a', Knowledge.MaxQueryLength + 1)}", "q=routine&k=0", "q=routine&k=11" })
            Assert.Equal(HttpStatusCode.BadRequest, (await client.GetAsync($"/api/knowledge/search?{query}")).StatusCode);
    }

    [Fact]
    public async Task Search_RanksTheMatchingContentFirst()
    {
        using (var scope = factory.Services.CreateScope())
            await Knowledge.IngestAsync(scope.ServiceProvider.GetRequiredService<AppDbContext>(),
                scope.ServiceProvider.GetRequiredService<IEmbedder>(), Knowledge.BuildChunks(EnglishUp.Api.Content.ReadSeed(Content)));
        var client = await factory.SignedInClient();

        var hits = await client.GetFromJsonAsync<List<SearchHit>>("/api/knowledge/search?q=routine&k=3");
        Assert.Equal(3, hits!.Count);
        Assert.Equal(("word", "routine"), (hits[0].SourceType, hits[0].Title));
        Assert.True(hits[0].Score > hits[1].Score);

        var plans = await client.GetFromJsonAsync<List<SearchHit>>(
            "/api/knowledge/search?q=" + Uri.EscapeDataString("Mai Ben Saturday birthday gift bookshop"));
        Assert.Equal(("listening", "l1"), (plans![0].SourceType, plans[0].SourceId));

        var pattern = await client.GetFromJsonAsync<List<SearchHit>>(
            "/api/knowledge/search?q=" + Uri.EscapeDataString("enjoy painting or enjoy to paint"));
        // The fake embedder only counts shared words, so assert the pattern reaches the tutor's five sources.
        Assert.Contains(pattern!, h => (h.SourceType, h.SourceId) == ("grammar", "s026"));
        Assert.Equal(5, plans.Count);
    }

    [Fact]
    public async Task Search_ReportsAQuotaLimitAs503()
    {
        var embedder = (FakeEmbedder)factory.Services.GetRequiredService<IEmbedder>();
        embedder.Failure = HttpStatusCode.TooManyRequests;
        try
        {
            var response = await (await factory.SignedInClient()).GetAsync("/api/knowledge/search?q=routine");
            Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode);
            Assert.Contains("quota", await response.Content.ReadAsStringAsync());
        }
        finally
        {
            embedder.Failure = null;
        }
    }
}
