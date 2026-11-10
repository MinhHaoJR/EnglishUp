using System.Security.Claims;
using System.Text.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api;

public record WordCard(string Id, string Word, string Meaning, string Level);

/// <summary>A question as stored on the server; the answer index never leaves it.</summary>
public record GameQuestion(string WordId, string Word, string[] Options, int Answer);

public record StartGameRequest(string? Level);

public record GameQuestionDto(string Word, string[] Options);

public record GameStartDto(Guid Id, int DurationSeconds, List<GameQuestionDto> Questions);

public record AnswerRequest(int Index, int Choice);

public record AnswerDto(bool Correct, int Answer, int Combo, int Score);

public record GameResultDto(int Score, int Correct, int Answered, int MaxCombo, int PointsEarned, int Best, bool IsRecord);

public record GameRecordsDto(int Best, int Played);

/// <summary>English words with Vietnamese meanings, from the content library in the database.</summary>
public class QuestionBank(IReadOnlyList<WordCard> words)
{
    private static readonly JsonSerializerOptions Web = new(JsonSerializerDefaults.Web);

    /// <summary>The visible word rows; incomplete rows and unknown levels are skipped, as the app skips them.</summary>
    public static QuestionBank From(IEnumerable<ContentItem> rows) => new(rows
        .Where(r => r is { Kind: "word", Hidden: false })
        .Select(r =>
        {
            try
            {
                return JsonSerializer.Deserialize<WordCard>(r.Json, Web);
            }
            catch (JsonException)
            {
                return null;
            }
        })
        .OfType<WordCard>()
        .Where(c => c is { Id.Length: > 0, Word.Length: > 0, Meaning.Length: > 0 } && Game.Levels.Contains(c.Level))
        .ToList());

    public int Count(string? level) => words.Count(w => level is null || w.Level == level);

    /// <summary>Distinct words at the level, each with its meaning and three other meanings in random order.</summary>
    public List<GameQuestion> Draw(string? level, int count, Random random)
    {
        var pool = words.Where(w => level is null || w.Level == level).OrderBy(_ => random.Next()).Take(count);
        return pool.Select(word =>
        {
            var options = words.Select(w => w.Meaning).Where(m => m != word.Meaning).Distinct()
                .OrderBy(_ => random.Next()).Take(3).Append(word.Meaning).OrderBy(_ => random.Next()).ToArray();
            return new GameQuestion(word.Id, word.Word, options, Array.IndexOf(options, word.Meaning));
        }).ToList();
    }
}

/// <summary>60-second multiple-choice race. The server draws, times and grades every answer.</summary>
public static class Game
{
    public const int DurationSeconds = 60;
    private const int QuestionCount = 60;
    // Allows for the request that was in flight when the learner's timer reached zero.
    private static readonly TimeSpan Grace = TimeSpan.FromSeconds(3);
    internal static readonly string[] Levels = ["A1", "A2", "B1", "B2", "C1", "C2"];

    public static int ScoreOf(int correct, int maxCombo) => 10 * correct + 5 * maxCombo;

    /// <summary>Ledger points for a finished game, before the shared daily cap.</summary>
    public static int PointsFor(int score) => score / 10;

    public static void MapGame(this IEndpointRouteBuilder api)
    {
        var game = api.MapGroup("/game").RequireAuthorization();

        game.MapPost("/start", async (StartGameRequest request, ClaimsPrincipal user, AppDbContext db,
            ContentStore store, TimeProvider clock) =>
        {
            if (request.Level is not null && !Levels.Contains(request.Level))
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["level"] = ["Unknown level."] });
            var questions = QuestionBank.From((await store.GetAsync(db)).Rows).Draw(request.Level, QuestionCount, Random.Shared);
            var session = new GameSession
            {
                Id = Guid.NewGuid(), UserId = UserId(user), Level = request.Level,
                QuestionsJson = JsonSerializer.Serialize(questions), StartedAt = clock.GetUtcNow(),
            };
            db.GameSessions.Add(session);
            await db.SaveChangesAsync();
            return Results.Ok(new GameStartDto(session.Id, DurationSeconds,
                questions.Select(q => new GameQuestionDto(q.Word, q.Options)).ToList()));
        });

        game.MapPost("/{id:guid}/answer", async (Guid id, AnswerRequest request, ClaimsPrincipal user,
            AppDbContext db, TimeProvider clock) =>
        {
            var session = await db.GameSessions.SingleOrDefaultAsync(s => s.Id == id && s.UserId == UserId(user));
            if (session is null) return Results.NotFound();
            if (session.FinishedAt is not null || clock.GetUtcNow() > session.StartedAt.AddSeconds(DurationSeconds) + Grace)
                return Results.Problem("Time is up.", statusCode: StatusCodes.Status409Conflict);
            var questions = JsonSerializer.Deserialize<List<GameQuestion>>(session.QuestionsJson)!;
            if (request.Index != session.Answered || request.Index >= questions.Count)
                return Results.Problem("Answer the current question.", statusCode: StatusCodes.Status409Conflict);
            if (request.Choice is < 0 or > 3)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["choice"] = ["Choose 0–3."] });

            var answer = questions[request.Index].Answer;
            var correct = request.Choice == answer;
            session.Answered++;
            session.Combo = correct ? session.Combo + 1 : 0;
            if (correct) session.Correct++;
            session.MaxCombo = Math.Max(session.MaxCombo, session.Combo);
            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                // Two answers for the same question arrived together; only the first counts.
                return Results.Problem("Answer the current question.", statusCode: StatusCodes.Status409Conflict);
            }
            return Results.Ok(new AnswerDto(correct, answer, session.Combo, ScoreOf(session.Correct, session.MaxCombo)));
        });

        game.MapPost("/{id:guid}/finish", async (Guid id, ClaimsPrincipal user, AppDbContext db, TimeProvider clock) =>
        {
            var userId = UserId(user);
            var session = await db.GameSessions.SingleOrDefaultAsync(s => s.Id == id && s.UserId == userId);
            if (session is null) return Results.NotFound();
            var previousBest = await db.GameSessions
                .Where(s => s.UserId == userId && s.Id != id && s.Score != null).MaxAsync(s => s.Score) ?? 0;

            if (session.FinishedAt is null)
            {
                var now = clock.GetUtcNow();
                session.FinishedAt = now;
                session.Score = ScoreOf(session.Correct, session.MaxCombo);
                var today = Points.Today(now);
                var points = Math.Min(PointsFor(session.Score.Value), await Points.RemainingTodayAsync(db, userId, today));
                if (points > 0)
                    db.PointLedger.Add(new PointEntry
                    {
                        UserId = userId, Source = "game", SourceId = id.ToString(),
                        Points = points, LocalDate = today, CreatedAt = now,
                    });
                await db.SaveChangesAsync();
            }

            var earned = await db.PointLedger
                .Where(p => p.UserId == userId && p.Source == "game" && p.SourceId == id.ToString()).SumAsync(p => p.Points);
            var score = session.Score!.Value;
            return Results.Ok(new GameResultDto(score, session.Correct, session.Answered, session.MaxCombo, earned,
                Math.Max(score, previousBest), score > previousBest));
        });

        game.MapGet("/records", async (ClaimsPrincipal user, AppDbContext db) =>
        {
            var finished = db.GameSessions.Where(s => s.UserId == UserId(user) && s.Score != null);
            return Results.Ok(new GameRecordsDto(await finished.MaxAsync(s => s.Score) ?? 0, await finished.CountAsync()));
        });
    }

    private static string UserId(ClaimsPrincipal user) => user.FindFirstValue(ClaimTypes.NameIdentifier)!;
}
