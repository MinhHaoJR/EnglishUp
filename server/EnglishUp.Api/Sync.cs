using System.Security.Claims;
using System.Text.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record AttemptDto(
    string Id, string Skill, double Score, double Duration, double Timestamp, string Label, string? LearningLanguage);

public record RecordDto(string Store, string Id, double Version, JsonElement Data);

public record SyncPayload(List<AttemptDto> Attempts, List<RecordDto> Records);

public static class Sync
{
    private static readonly HashSet<string> Stores =
        ["settings", "words", "reviews", "drafts", "submissions", "vocabularyStudy"];
    private static readonly HashSet<string> Skills = ["vocabulary", "listening", "speaking", "reading", "writing"];
    private static readonly HashSet<string> Languages = ["en", "ja", "zh"];
    private const int MaxRecordLength = 200_000;

    public static void MapSync(this IEndpointRouteBuilder api) =>
        api.MapPost("/sync", Merge).RequireAuthorization();

    /// <summary>
    /// Merges the device's records into the account and returns the account's full state.
    /// Attempts are append-only by id; other records keep the highest version (last write wins).
    /// </summary>
    private static async Task<IResult> Merge(SyncPayload payload, ClaimsPrincipal user, AppDbContext db)
    {
        var errors = Validate(payload);
        if (errors.Count > 0) return Results.ValidationProblem(errors);
        var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

        var attemptIds = (await db.Attempts.Where(a => a.UserId == userId).Select(a => a.Id).ToListAsync())
            .ToHashSet();
        foreach (var a in payload.Attempts.Where(a => attemptIds.Add(a.Id)))
            db.Attempts.Add(new Attempt
            {
                UserId = userId, Id = a.Id, Skill = a.Skill, Score = a.Score, Duration = a.Duration,
                Timestamp = a.Timestamp, Label = a.Label, LearningLanguage = a.LearningLanguage,
            });

        var records = await db.SyncRecords.Where(r => r.UserId == userId).ToDictionaryAsync(r => (r.Store, r.Id));
        foreach (var incoming in payload.Records)
        {
            if (!records.TryGetValue((incoming.Store, incoming.Id), out var record))
            {
                record = new SyncRecord
                {
                    UserId = userId, Store = incoming.Store, Id = incoming.Id,
                    Version = incoming.Version, Data = incoming.Data.GetRawText(),
                };
                records.Add((record.Store, record.Id), record);
                db.SyncRecords.Add(record);
            }
            else if (incoming.Version > record.Version)
            {
                record.Version = incoming.Version;
                record.Data = incoming.Data.GetRawText();
            }
        }

        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException)
        {
            // Another device inserted the same record at the same moment; its next sync succeeds.
            return Results.Conflict();
        }

        // shortcut: returns the whole account every time; add a since-cursor once histories reach many MB.
        var attempts = await db.Attempts.Where(a => a.UserId == userId).OrderBy(a => a.Timestamp)
            .Select(a => new AttemptDto(a.Id, a.Skill, a.Score, a.Duration, a.Timestamp, a.Label, a.LearningLanguage))
            .ToListAsync();
        return Results.Ok(new SyncPayload(attempts, records.Values
            .Select(r => new RecordDto(r.Store, r.Id, r.Version, JsonDocument.Parse(r.Data).RootElement.Clone()))
            .ToList()));
    }

    private static Dictionary<string, string[]> Validate(SyncPayload payload)
    {
        var errors = new Dictionary<string, string[]>();
        void Check(bool ok, string key, string message)
        {
            if (!ok) errors.TryAdd(key, [message]);
        }
        Check(payload.Attempts is not null && payload.Records is not null, "payload", "attempts and records are required.");
        if (errors.Count > 0) return errors;

        for (var i = 0; i < payload.Attempts.Count; i++)
        {
            var a = payload.Attempts[i];
            var key = $"attempts[{i}]";
            Check(ValidId(a.Id), key, "Invalid id.");
            Check(Skills.Contains(a.Skill ?? ""), key, "Unknown skill.");
            Check(a.Score is >= 0 and <= 100, key, "Score must be 0–100.");
            Check(a.Duration >= 0 && a.Timestamp >= 0, key, "Duration and timestamp must not be negative.");
            Check(a.Label is { Length: <= 500 }, key, "Label is required and at most 500 characters.");
            Check(a.LearningLanguage is null || Languages.Contains(a.LearningLanguage), key, "Unknown language.");
        }
        for (var i = 0; i < payload.Records.Count; i++)
        {
            var r = payload.Records[i];
            var key = $"records[{i}]";
            Check(Stores.Contains(r.Store ?? ""), key, "Unknown store.");
            Check(ValidId(r.Id), key, "Invalid id.");
            Check(r.Version >= 0, key, "Version must not be negative.");
            Check(r.Data.ValueKind == JsonValueKind.Object && r.Data.GetRawText().Length <= MaxRecordLength,
                key, "Data must be a JSON object under 200,000 characters.");
        }
        return errors;
    }

    private static bool ValidId(string? id) => id is { Length: > 0 and <= 128 };
}
