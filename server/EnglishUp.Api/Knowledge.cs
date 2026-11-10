using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Pgvector;
using Pgvector.EntityFrameworkCore;

namespace EnglishUp.Api;

/// <summary>One piece of learning content before it is embedded.</summary>
public record ChunkSource(string SourceType, string SourceId, string Title, string Text)
{
    public string Hash => Convert.ToHexStringLower(SHA256.HashData(Encoding.UTF8.GetBytes(Title + "\n" + Text)));
}

public record SearchHit(int ChunkId, string SourceType, string SourceId, string Title, string Text, double Score);

/// <summary>Remaining: chunks still to embed because the run hit its <c>max</c>.</summary>
public record IngestReport(int Added, int Updated, int Unchanged, int Removed, int Remaining = 0);

/// <summary>Turns text into vectors; Gemini in the app, a deterministic fake in tests.</summary>
public interface IEmbedder
{
    string Model { get; }
    Task<float[][]> EmbedDocumentsAsync(IReadOnlyList<ChunkSource> chunks, CancellationToken ct = default);
    Task<float[]> EmbedQueryAsync(string query, CancellationToken ct = default);
}

/// <summary>Gemini embedContent client; the key comes from user-secrets or the environment, never the client.</summary>
public class GeminiEmbedder(HttpClient http, IConfiguration config) : IEmbedder
{
    public const int Dimensions = 768;
    private const int BatchLimit = 100;
    public string Model => config["Gemini:EmbeddingModel"] ?? "gemini-embedding-2";

    // gemini-embedding-2 takes no task_type; the docs ask for these prefixes instead.
    public Task<float[][]> EmbedDocumentsAsync(IReadOnlyList<ChunkSource> chunks, CancellationToken ct = default) =>
        EmbedAsync(chunks.Select(c => $"title: {c.Title} | text: {c.Text}").ToList(), ct);

    public async Task<float[]> EmbedQueryAsync(string query, CancellationToken ct = default) =>
        (await EmbedAsync([$"task: question answering | query: {query}"], ct))[0];

    private async Task<float[][]> EmbedAsync(IReadOnlyList<string> texts, CancellationToken ct)
    {
        var vectors = new List<float[]>();
        foreach (var batch in texts.Chunk(BatchLimit))
        {
            var body = await Gemini.PostAsync<BatchResponse>(http, config, Model, "batchEmbedContents", new
            {
                requests = batch.Select(text => new
                {
                    model = $"models/{Model}",
                    content = new { parts = new[] { new { text } } },
                    outputDimensionality = Dimensions,
                }),
            }, ct);
            vectors.AddRange(body.Embeddings.Select(e => e.Values));
        }
        return [.. vectors];
    }

    private record BatchResponse(List<Embedding> Embeddings);
    private record Embedding(float[] Values);
}

/// <summary>Retrieval for the RAG assistant: the app's own learning content, embedded and searched by cosine similarity.</summary>
public static class Knowledge
{
    public const int MaxQueryLength = 500;
    public const int MaxResults = 10;

    private record ContentWord(string Id, string Word, string Ipa, string Pos, string Meaning, string Definition,
        string[] Examples, string Level, string Topic);
    private record ContentReading(string Id, string Title, string Level, string Topic, string Text);
    private record Line(string Speaker, string Text);
    private record ContentListening(string Id, string Title, string Level, string Topic, Line[] Lines);
    private record ContentWriting(string Id, string Title, string Level, string Topic, string Genre, string Prompt,
        int MinWords, int MaxWords, string[] Checklist);
    private record ContentPattern(string Id, string Formula, string Meaning, string Example, string Key,
        string[] Options, string Translation);

    /// <summary>The bundled learning content shipped next to the API (linked from src/data).</summary>
    public static readonly string Folder = Path.Combine(AppContext.BaseDirectory, "Content");

    /// <summary>Content kinds the assistant knows, with their chunk source type; dictation and speaking are not taught content.</summary>
    public static readonly Dictionary<string, string> SourceTypes = new()
    {
        ["reading"] = "reading", ["listening"] = "listening", ["writing"] = "writing", ["structure"] = "grammar", ["word"] = "word",
    };

    private static readonly Dictionary<string, string[]> Files = new()
    {
        ["reading"] = ["reading.json"], ["listening"] = ["listening.json"], ["writing"] = ["writing.json"],
        ["structure"] = ["structures.json"], ["word"] = ["vocabulary.json", "vocabulary-it.json"],
    };

    private static readonly JsonSerializerOptions Web = new(JsonSerializerDefaults.Web);

    /// <summary>
    /// One chunk per word, reading, listening script, writing task and sentence pattern; each stays well under 300 words.
    /// Admin rows (<see cref="ContentItem"/>) sit on top of the bundled files, as in the app: same id replaces, hidden removes.
    /// </summary>
    public static List<ChunkSource> BuildChunks(string folder, IEnumerable<ContentItem>? overlay = null)
    {
        var rows = overlay?.ToList() ?? [];
        // Lessons first: with 1,000 free embeddings a day, a first ingest spans several days.
        return Files.SelectMany(kind =>
        {
            var items = new List<(string Id, JsonElement Item)>();
            foreach (var file in kind.Value)
                items.AddRange(JsonSerializer.Deserialize<List<JsonElement>>(File.ReadAllText(Path.Combine(folder, file)))!
                    .Select(e => (e.GetProperty("id").GetString()!, e)));
            foreach (var row in rows.Where(r => r.Kind == kind.Key))
            {
                var at = items.FindIndex(i => i.Id == row.Id);
                if (row.Hidden || row.Json is null)
                {
                    if (row.Hidden && at >= 0) items.RemoveAt(at);
                    continue;
                }
                var item = (row.Id, JsonDocument.Parse(row.Json).RootElement.Clone());
                if (at >= 0) items[at] = item;
                else items.Add(item);
            }
            return items.Select(i => ToChunk(kind.Key, i.Item)).OfType<ChunkSource>();
        }).ToList();
    }

    /// <summary>The chunk for one item, or null when an admin row lacks what the text needs (the app skips it too).</summary>
    public static ChunkSource? ToChunk(string kind, JsonElement item)
    {
        try
        {
            return kind switch
            {
                "word" => Word(item.Deserialize<ContentWord>(Web)!),
                "reading" => item.Deserialize<ContentReading>(Web) is { } r
                    ? new ChunkSource("reading", r.Id, r.Title, $"Reading lesson ({r.Level}, {r.Topic}).\n{r.Text}") : null,
                "listening" => item.Deserialize<ContentListening>(Web) is { } l
                    ? new ChunkSource("listening", l.Id, l.Title,
                        $"Listening script ({l.Level}, {l.Topic}).\n" + string.Join("\n", l.Lines.Select(x => $"{x.Speaker}: {x.Text}")))
                    : null,
                "writing" => item.Deserialize<ContentWriting>(Web) is { } w
                    ? new ChunkSource("writing", w.Id, w.Title,
                        $"Writing task: {w.Genre}, {w.Level}, {w.Topic}, {w.MinWords}-{w.MaxWords} words.\n{w.Prompt}\n" +
                        $"Checklist: {string.Join(" ", w.Checklist)}")
                    : null,
                // The quiz's wrong forms are named as such, so questions like "enjoy + to-V?" find the pattern.
                "structure" => item.Deserialize<ContentPattern>(Web) is { } p
                    ? new ChunkSource("grammar", p.Id, p.Formula,
                        $"Sentence pattern: {p.Formula}\nVietnamese meaning: {p.Meaning}\n" +
                        $"Example: {p.Example} (the pattern in use: \"{p.Key}\")\nVietnamese translation: {p.Translation}\n" +
                        $"Wrong forms learners often use: {string.Join("; ", p.Options)}")
                    : null,
                _ => null,
            } is { SourceId: not null and not "", Title: not null and not "" } chunk ? chunk : null;
        }
        catch (Exception e) when (e is JsonException or ArgumentNullException or NullReferenceException)
        {
            return null;
        }
    }

    private static ChunkSource Word(ContentWord w) => new("word", w.Id, w.Word,
        $"{w.Word} ({w.Pos}, level {w.Level}, topic {w.Topic}){(string.IsNullOrEmpty(w.Ipa) ? "" : $" {w.Ipa}")}\n" +
        $"Vietnamese meaning: {w.Meaning}\nDefinition: {w.Definition}\nExamples: {string.Join(" ", w.Examples)}");

    /// <summary>
    /// Embeds only new or changed chunks and removes ones no longer in the content, so a run cut short by a
    /// rate limit can simply be repeated. Saves after each batch to keep the progress.
    /// The free tier allows 100 embeddings a minute, so a 429 waits <paramref name="retryAfter"/> (default 61 s)
    /// and retries, up to <see cref="Gemini.MaxTries"/> in a row; the daily quota (1,000) stops at once.
    /// </summary>
    public static async Task<IngestReport> IngestAsync(AppDbContext db, IEmbedder embedder, IReadOnlyList<ChunkSource> sources,
        Action<string>? log = null, int batchSize = 100, TimeSpan? retryAfter = null, int? max = null, CancellationToken ct = default)
    {
        var existing = await db.KnowledgeChunks.ToDictionaryAsync(c => (c.SourceType, c.SourceId), ct);
        var wanted = sources.ToDictionary(s => (s.SourceType, s.SourceId));
        var stale = existing.Values.Where(c => !wanted.ContainsKey((c.SourceType, c.SourceId))).ToList();
        db.KnowledgeChunks.RemoveRange(stale);
        await db.SaveChangesAsync(ct);

        var todo = sources.Where(s => !existing.TryGetValue((s.SourceType, s.SourceId), out var c)
            || c.ContentHash != s.Hash || c.EmbeddingModel != embedder.Model).ToList();
        var pending = todo.Count;
        todo = todo.Take(max ?? int.MaxValue).ToList();
        int added = 0, updated = 0;
        foreach (var batch in todo.Chunk(batchSize))
        {
            var vectors = await Gemini.WithRetryAsync(() => embedder.EmbedDocumentsAsync(batch, ct), retryAfter, log, ct);
            for (var i = 0; i < batch.Length; i++)
            {
                var source = batch[i];
                if (!existing.TryGetValue((source.SourceType, source.SourceId), out var chunk))
                {
                    chunk = new KnowledgeChunk
                    {
                        SourceType = source.SourceType, SourceId = source.SourceId, Title = source.Title,
                        Text = source.Text, ContentHash = "", EmbeddingModel = "", Embedding = null!,
                    };
                    db.KnowledgeChunks.Add(chunk);
                    added++;
                }
                else updated++;
                chunk.Title = source.Title;
                chunk.Text = source.Text;
                chunk.ContentHash = source.Hash;
                chunk.EmbeddingModel = embedder.Model;
                chunk.Embedding = new Vector(vectors[i]);
            }
            await db.SaveChangesAsync(ct);
            log?.Invoke($"Embedded {added + updated}/{todo.Count} chunks");
        }
        return new IngestReport(added, updated, sources.Count - pending, stale.Count, pending - todo.Count);
    }

    /// <summary>
    /// Re-embeds the one item an admin just changed, so the assistant answers from it at once (one embedding call).
    /// If Gemini is unreachable the change is still saved; the next <c>ingest</c> picks it up.
    /// </summary>
    public static async Task SyncAsync(AppDbContext db, IEmbedder embedder, string kind, string id, CancellationToken ct = default)
    {
        if (!SourceTypes.TryGetValue(kind, out var type)) return;
        var rows = await db.ContentItems.Where(c => c.Kind == kind && c.Id == id).ToListAsync(ct);
        var source = BuildChunks(Folder, rows).SingleOrDefault(c => c.SourceType == type && c.SourceId == id);
        var chunk = await db.KnowledgeChunks.SingleOrDefaultAsync(c => c.SourceType == type && c.SourceId == id, ct);
        if (source is null)
        {
            if (chunk is not null) db.KnowledgeChunks.Remove(chunk);
        }
        else if (chunk?.ContentHash != source.Hash || chunk.EmbeddingModel != embedder.Model)
        {
            var vector = (await embedder.EmbedDocumentsAsync([source], ct))[0];
            if (chunk is null)
                db.KnowledgeChunks.Add(chunk = new KnowledgeChunk
                {
                    SourceType = type, SourceId = id, Title = "", Text = "", ContentHash = "", EmbeddingModel = "", Embedding = null!,
                });
            chunk.Title = source.Title;
            chunk.Text = source.Text;
            chunk.ContentHash = source.Hash;
            chunk.EmbeddingModel = embedder.Model;
            chunk.Embedding = new Vector(vector);
        }
        await db.SaveChangesAsync(ct);
    }

    /// <summary>The k chunks closest to the query by cosine similarity (1 = same direction).</summary>
    public static async Task<List<SearchHit>> SearchAsync(AppDbContext db, IEmbedder embedder, string query, int k,
        CancellationToken ct = default)
    {
        var vector = new Vector(await embedder.EmbedQueryAsync(query, ct));
        if (db.Database.IsNpgsql())
            return await db.KnowledgeChunks
                .Select(c => new { c, Distance = c.Embedding.CosineDistance(vector) })
                .OrderBy(x => x.Distance).Take(k)
                .Select(x => new SearchHit(x.c.Id, x.c.SourceType, x.c.SourceId, x.c.Title, x.c.Text, 1 - x.Distance))
                .ToListAsync(ct);
        // shortcut: the in-memory test database cannot run pgvector SQL, so tests rank in C#; Postgres uses the HNSW index.
        var q = vector.ToArray();
        return (await db.KnowledgeChunks.ToListAsync(ct))
            .Select(c => new SearchHit(c.Id, c.SourceType, c.SourceId, c.Title, c.Text, Cosine(q, c.Embedding.ToArray())))
            .OrderByDescending(h => h.Score).Take(k).ToList();
    }

    public static double Cosine(float[] a, float[] b)
    {
        double dot = 0, na = 0, nb = 0;
        for (var i = 0; i < a.Length; i++) { dot += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
        return na == 0 || nb == 0 ? 0 : dot / Math.Sqrt(na * nb);
    }

    public static void MapKnowledge(this RouteGroupBuilder api)
    {
        // Signed-in only: every search spends one embedding call from the shared Gemini quota.
        api.MapGet("/knowledge/search", async (string? q, int? k, AppDbContext db, IEmbedder embedder, CancellationToken ct) =>
        {
            var query = q?.Trim() ?? "";
            var count = k ?? 5;
            if (query.Length is 0 or > MaxQueryLength || count is < 1 or > MaxResults)
                return Results.ValidationProblem(new Dictionary<string, string[]>
                {
                    ["q"] = [$"Enter 1–{MaxQueryLength} characters and ask for 1–{MaxResults} results."],
                });
            try
            {
                return Results.Ok(await SearchAsync(db, embedder, query, count, ct));
            }
            catch (HttpRequestException e)
            {
                return Gemini.Unavailable(e);
            }
        }).RequireAuthorization();
    }
}
