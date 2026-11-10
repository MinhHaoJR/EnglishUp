using System.Security.Claims;
using System.Text.Json;
using System.Text.RegularExpressions;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record ContentItemDto(string Kind, string Id, JsonElement? Data, bool Hidden, DateTimeOffset UpdatedAt);
public record ContentSaveRequest(JsonElement Data);
public record ContentHideRequest(bool Hidden);

/// <summary>
/// Learning content added, edited or hidden by admins. The bundled JSON in src/data stays the base;
/// these rows sit on top of it (same kind and id replaces a bundled item, a hidden row removes it).
/// Every client validates each item with the app's own schemas before use, so a bad row is skipped,
/// never shown; the server checks the envelope and the required fields.
/// </summary>
public static partial class Content
{
    private const int MaxJsonLength = 64 * 1024;

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
    };

    [GeneratedRegex("^[A-Za-z0-9-]{1,64}$")]
    private static partial Regex IdPattern();

    public static void MapContent(this IEndpointRouteBuilder api)
    {
        // Public: signed-out learners practise with the same lessons.
        api.MapGet("/content", async (AppDbContext db) =>
            Results.Ok((await db.ContentItems.AsNoTracking().OrderBy(c => c.Kind).ThenBy(c => c.Id).ToListAsync())
                .Select(ToDto)));

        var admin = api.MapGroup("/admin/content").RequireAuthorization(Admin.Policy);

        admin.MapPut("/{kind}/{id}", async (string kind, string id, ContentSaveRequest input, ClaimsPrincipal user,
            AppDbContext db, IEmbedder embedder, ILoggerFactory logs, TimeProvider clock) =>
        {
            var errors = Validate(kind, id, input.Data);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            var row = await db.ContentItems.FindAsync(kind, id);
            if (row is null) db.ContentItems.Add(row = new ContentItem { Kind = kind, Id = id });
            row.Json = input.Data.GetRawText();
            row.Hidden = false;
            row.UpdatedAt = clock.GetUtcNow();
            row.UpdatedBy = user.FindFirstValue(ClaimTypes.Name) ?? "";
            await db.SaveChangesAsync();
            await ReindexAsync(db, embedder, logs, kind, id);
            return Results.Ok(ToDto(row));
        });

        admin.MapPost("/{kind}/{id}/hide", async (string kind, string id, ContentHideRequest input, ClaimsPrincipal user,
            AppDbContext db, IEmbedder embedder, ILoggerFactory logs, TimeProvider clock) =>
        {
            if (!Required.ContainsKey(kind) || !IdPattern().IsMatch(id)) return Results.BadRequest();
            var row = await db.ContentItems.FindAsync(kind, id);
            // Showing a bundled item that was only hidden: nothing is left to keep, so the row goes.
            if (row is { Json: null } && !input.Hidden)
            {
                db.ContentItems.Remove(row);
                await db.SaveChangesAsync();
                await ReindexAsync(db, embedder, logs, kind, id);
                return Results.NoContent();
            }
            if (row is null) db.ContentItems.Add(row = new ContentItem { Kind = kind, Id = id });
            row.Hidden = input.Hidden;
            row.UpdatedAt = clock.GetUtcNow();
            row.UpdatedBy = user.FindFirstValue(ClaimTypes.Name) ?? "";
            await db.SaveChangesAsync();
            await ReindexAsync(db, embedder, logs, kind, id);
            return Results.Ok(ToDto(row));
        });

        // Removes the admin's row: an added item disappears, an edited bundled item returns to the original.
        admin.MapDelete("/{kind}/{id}", async (string kind, string id, AppDbContext db, IEmbedder embedder,
            ILoggerFactory logs) =>
        {
            var row = await db.ContentItems.FindAsync(kind, id);
            if (row is null) return Results.NotFound();
            db.ContentItems.Remove(row);
            await db.SaveChangesAsync();
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

    private static ContentItemDto ToDto(ContentItem row) => new(
        row.Kind, row.Id,
        row.Json is null ? null : JsonDocument.Parse(row.Json).RootElement.Clone(),
        row.Hidden, row.UpdatedAt);
}
