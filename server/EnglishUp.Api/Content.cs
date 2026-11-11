using System.Security.Claims;
using System.Text.Json;
using System.Text.RegularExpressions;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record ContentItemDto(string Kind, string Id, JsonElement Data, bool Hidden, DateTimeOffset UpdatedAt);
public record ContentSaveRequest(JsonElement Data);
public record ContentHideRequest(bool Hidden);
public record SeedReport(int Added, int Updated, int Unchanged);

/// <summary>
/// Every English learning item lives in the ContentItems table: the app, the 60-second race and the RAG assistant
/// all read it from here. The JSON in src/data is only seed data for an empty database (the <c>seed</c> command) and tests.
/// Every client validates each item with the app's own schemas before use, so a bad row is skipped, never shown;
/// the server checks the envelope and the required fields.
/// </summary>
public static partial class Content
{
    private const int MaxJsonLength = 64 * 1024;

    /// <summary>The seed JSON shipped next to the API (linked from src/data).</summary>
    public static readonly string SeedFolder = Path.Combine(AppContext.BaseDirectory, "Content");

    /// <summary>Fields each kind must have; the full shape is checked by the client's Zod schemas.</summary>
    public static readonly Dictionary<string, string[]> Required = new()
    {
        ["word"] = ["word", "pos", "meaning", "definition", "examples", "level", "topic"],
        ["structure"] = ["group", "formula", "meaning", "example", "key", "options", "translation"],
        ["reading"] = ["title", "level", "topic", "text", "questions"],
        ["listening"] = ["title", "level", "topic", "lines", "questions"],
        ["dictation"] = ["text", "level", "topic"],
        ["speaking"] = ["title", "level", "topic", "mode", "text", "cues"],
        ["writing"] = ["title", "level", "topic", "genre", "prompt", "minWords", "maxWords", "checklist"],
        ["translation"] = ["level", "topic", "en", "vi"],
        ["relation"] = ["level", "word", "pos", "meaning", "definition", "example", "synonyms", "antonyms", "usageNote"],
        ["quiz"] = ["level", "category", "sentence", "options", "answer", "explanation"],
        ["roadmap"] = ["from", "to", "weeks", "title", "summary", "stages"],
        ["tense"] = ["order", "group", "level", "name", "forms", "uses", "signals", "tip", "practice"],
        ["guide"] = ["category", "question", "answer"],
    };

    /// <summary>Seed files per kind, in the order the app lists them.</summary>
    public static readonly Dictionary<string, string[]> SeedFiles = new()
    {
        ["word"] = ["vocabulary.json", "vocabulary-it.json", "vocabulary-phrasal.json", "vocabulary-collocations.json", "vocabulary-verbs.json"],
        ["structure"] = ["structures.json"],
        ["reading"] = ["reading.json"],
        ["listening"] = ["listening.json"],
        ["dictation"] = ["dictation.json"],
        ["speaking"] = ["speaking.json"],
        ["writing"] = ["writing.json"],
        ["translation"] = ["translations.json"],
        ["relation"] = ["wordRelations-basic.json", "wordRelations-advanced.json"],
        ["quiz"] = ["grammar-quiz.json"],
        ["roadmap"] = ["roadmaps.json"],
        ["tense"] = ["tenses.json"],
        ["guide"] = ["guides.json"],
    };

    [GeneratedRegex("^[A-Za-z0-9-]{1,64}$")]
    private static partial Regex IdPattern();

    /// <summary>The seed files as rows, numbered in file order within each kind.</summary>
    public static List<ContentItem> ReadSeed(string folder) =>
        SeedFiles.SelectMany(kind => kind.Value
            .SelectMany(file => JsonSerializer.Deserialize<List<JsonElement>>(File.ReadAllText(Path.Combine(folder, file)))!)
            .Select((item, position) => new ContentItem
            {
                Kind = kind.Key, Id = item.GetProperty("id").GetString()!, Json = item.GetRawText(), Position = position,
                UpdatedBy = "seed",
            })).ToList();

    /// <summary>
    /// Adds seed items the database lacks. Existing rows (an admin's edits) stay unless <paramref name="overwrite"/>,
    /// which puts the seed's text and order back on the items that are in the seed.
    /// </summary>
    public static async Task<SeedReport> SeedAsync(AppDbContext db, string folder, DateTimeOffset now, bool overwrite = false)
    {
        var existing = await db.ContentItems.ToDictionaryAsync(c => (c.Kind, c.Id));
        int added = 0, updated = 0, unchanged = 0;
        foreach (var seed in ReadSeed(folder))
        {
            if (!existing.TryGetValue((seed.Kind, seed.Id), out var row))
            {
                seed.UpdatedAt = now;
                db.ContentItems.Add(seed);
                added++;
            }
            else if (overwrite && (row.Json != seed.Json || row.Position != seed.Position))
            {
                (row.Json, row.Position, row.UpdatedAt, row.UpdatedBy) = (seed.Json, seed.Position, now, "seed");
                updated++;
            }
            else unchanged++;
        }
        await db.SaveChangesAsync();
        return new SeedReport(added, updated, unchanged);
    }

    public static void MapContent(this IEndpointRouteBuilder api)
    {
        // Public: signed-out learners practise with the same lessons. The ETag lets browsers revalidate
        // the whole library (about 1 MB) with a 304 instead of downloading it on every start.
        api.MapGet("/content", async (HttpContext http, AppDbContext db, ContentStore store) =>
        {
            var (rows, version) = await store.GetAsync(db);
            http.Response.Headers.CacheControl = "no-cache";
            http.Response.Headers.ETag = version;
            if (http.Request.Headers.IfNoneMatch == version) return Results.StatusCode(StatusCodes.Status304NotModified);
            return Results.Ok(rows.Select(ToDto));
        });

        var admin = api.MapGroup("/admin/content").RequireAuthorization(Admin.Policy);

        admin.MapPut("/{kind}/{id}", async (string kind, string id, ContentSaveRequest input, ClaimsPrincipal user,
            AppDbContext db, ContentStore store, IEmbedder embedder, ILoggerFactory logs, TimeProvider clock) =>
        {
            var errors = Validate(kind, id, input.Data);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            var row = await db.ContentItems.FindAsync(kind, id);
            if (row is null)
            {
                // New items go to the end of their kind's list.
                var last = await db.ContentItems.Where(c => c.Kind == kind).MaxAsync(c => (int?)c.Position) ?? -1;
                db.ContentItems.Add(row = new ContentItem { Kind = kind, Id = id, Json = "", Position = last + 1 });
            }
            row.Json = input.Data.GetRawText();
            row.UpdatedAt = clock.GetUtcNow();
            row.UpdatedBy = user.FindFirstValue(ClaimTypes.Name) ?? "";
            await db.SaveChangesAsync();
            store.Invalidate();
            await ReindexAsync(db, embedder, logs, kind, id);
            return Results.Ok(ToDto(row));
        });

        admin.MapPost("/{kind}/{id}/hide", async (string kind, string id, ContentHideRequest input, ClaimsPrincipal user,
            AppDbContext db, ContentStore store, IEmbedder embedder, ILoggerFactory logs, TimeProvider clock) =>
        {
            var row = await db.ContentItems.FindAsync(kind, id);
            if (row is null) return Results.NotFound();
            row.Hidden = input.Hidden;
            row.UpdatedAt = clock.GetUtcNow();
            row.UpdatedBy = user.FindFirstValue(ClaimTypes.Name) ?? "";
            await db.SaveChangesAsync();
            store.Invalidate();
            await ReindexAsync(db, embedder, logs, kind, id);
            return Results.Ok(ToDto(row));
        });

        admin.MapDelete("/{kind}/{id}", async (string kind, string id, AppDbContext db, ContentStore store,
            IEmbedder embedder, ILoggerFactory logs) =>
        {
            var row = await db.ContentItems.FindAsync(kind, id);
            if (row is null) return Results.NotFound();
            db.ContentItems.Remove(row);
            await db.SaveChangesAsync();
            store.Invalidate();
            await ReindexAsync(db, embedder, logs, kind, id);
            return Results.NoContent();
        });
    }

    /// <summary>Keeps the assistant's chunk in step with the change; a Gemini failure leaves it for the next ingest.</summary>
    private static async Task ReindexAsync(AppDbContext db, IEmbedder embedder, ILoggerFactory logs, string kind, string id)
    {
        try
        {
            await Knowledge.SyncAsync(db, embedder, kind, id);
        }
        catch (Exception e) when (e is HttpRequestException or InvalidOperationException or TaskCanceledException)
        {
            db.ChangeTracker.Clear();
            logs.CreateLogger("Content").LogWarning(e, "Could not re-embed {Kind}/{Id}; run ingest later", kind, id);
        }
    }

    public static Dictionary<string, string[]> Validate(string kind, string id, JsonElement data)
    {
        var errors = new Dictionary<string, string[]>();
        if (!Required.TryGetValue(kind, out var fields))
            errors["kind"] = [$"Unknown kind; use one of {string.Join(", ", Required.Keys)}."];
        if (!IdPattern().IsMatch(id)) errors["id"] = ["Ids are 1–64 letters, digits or dashes."];
        if (data.ValueKind != JsonValueKind.Object)
        {
            errors["data"] = ["The item must be a JSON object."];
            return errors;
        }
        if (data.GetRawText().Length > MaxJsonLength) errors["data"] = ["The item is larger than 64 KB."];
        if (!data.TryGetProperty("id", out var itemId) || itemId.ValueKind != JsonValueKind.String || itemId.GetString() != id)
            errors["data.id"] = ["data.id must equal the id in the address."];
        foreach (var field in fields ?? [])
            if (!data.TryGetProperty(field, out var value) || value.ValueKind is JsonValueKind.Null or JsonValueKind.Undefined
                || (value.ValueKind == JsonValueKind.String && string.IsNullOrWhiteSpace(value.GetString())))
                errors[$"data.{field}"] = ["Required."];
        return errors;
    }

    private static ContentItemDto ToDto(ContentItem row) =>
        new(row.Kind, row.Id, JsonDocument.Parse(row.Json).RootElement.Clone(), row.Hidden, row.UpdatedAt);
}

/// <summary>
/// The content rows in memory, read from the database once and again after each admin change, so learners'
/// app starts and race games do not each pull the whole library from Supabase.
/// shortcut: one cache per API process; with several instances, another instance's admin change shows only
/// after that instance restarts. Upgrade to a version column checked per request if the API is scaled out.
/// </summary>
public class ContentStore
{
    private volatile Snapshot? current;
    private int generation;
    private record Snapshot(IReadOnlyList<ContentItem> Rows, string Version);

    public async Task<(IReadOnlyList<ContentItem> Rows, string Version)> GetAsync(AppDbContext db)
    {
        var snapshot = current;
        if (snapshot is null)
        {
            var started = Volatile.Read(ref generation);
            var rows = await db.ContentItems.AsNoTracking().OrderBy(c => c.Kind).ThenBy(c => c.Position).ThenBy(c => c.Id)
                .ToListAsync();
            var stamp = rows.Count == 0 ? 0 : rows.Max(r => r.UpdatedAt.UtcTicks);
            snapshot = new Snapshot(rows, $"\"{rows.Count}-{stamp}\"");
            // A change saved while this read ran keeps the cache empty, so the next request reads it.
            if (Volatile.Read(ref generation) == started) current = snapshot;
        }
        return (snapshot.Rows, snapshot.Version);
    }

    public void Invalidate()
    {
        Interlocked.Increment(ref generation);
        current = null;
    }
}
