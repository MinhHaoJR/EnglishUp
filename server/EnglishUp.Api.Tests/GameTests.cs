using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

public class GameTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private static async Task<GameStartDto> Start(HttpClient client, string? level = null)
    {
        var response = await client.PostAsJsonAsync("/api/game/start", new { level });
        response.EnsureSuccessStatusCode();
        return (await response.Content.ReadFromJsonAsync<GameStartDto>())!;
    }

    /// <summary>The answer key, which only the server knows.</summary>
    private async Task<List<GameQuestion>> Key(Guid id)
    {
        using var scope = factory.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        var json = await db.GameSessions.Where(s => s.Id == id).Select(s => s.QuestionsJson).SingleAsync();
        return JsonSerializer.Deserialize<List<GameQuestion>>(json)!;
    }

    private static Task<HttpResponseMessage> Answer(HttpClient client, Guid id, int index, int choice) =>
        client.PostAsJsonAsync($"/api/game/{id}/answer", new { index, choice });

    /// <summary>Answers in order; true means the right option, false a wrong one.</summary>
    private async Task Play(HttpClient client, Guid id, params bool[] right)
    {
        var key = await Key(id);
        for (var i = 0; i < right.Length; i++)
        {
            var choice = right[i] ? key[i].Answer : (key[i].Answer + 1) % 4;
            (await Answer(client, id, i, choice)).EnsureSuccessStatusCode();
        }
    }

    private static async Task<GameResultDto> Finish(HttpClient client, Guid id)
    {
        var response = await client.PostAsync($"/api/game/{id}/finish", null);
        response.EnsureSuccessStatusCode();
        return (await response.Content.ReadFromJsonAsync<GameResultDto>())!;
    }

    [Fact]
    public async Task Game_RequiresToken()
    {
        var response = await factory.CreateClient().PostAsJsonAsync("/api/game/start", new { level = (string?)null });
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task Start_SendsQuestionsWithoutAnswers()
    {
        var client = await factory.SignedInClient();
        var response = await client.PostAsJsonAsync("/api/game/start", new { level = (string?)null });
        var body = await response.Content.ReadAsStringAsync();
        using (var json = JsonDocument.Parse(body))
            Assert.All(json.RootElement.GetProperty("questions").EnumerateArray(), q =>
                Assert.Equal(["word", "options"], q.EnumerateObject().Select(p => p.Name)));

        var game = JsonSerializer.Deserialize<GameStartDto>(body, JsonSerializerOptions.Web)!;
        Assert.Equal(60, game.DurationSeconds);
        Assert.Equal(60, game.Questions.Count);
        Assert.Equal(60, game.Questions.Select(q => q.Word).Distinct().Count());
        Assert.All(game.Questions, q => Assert.Equal(4, q.Options.Distinct().Count()));
    }

    [Fact]
    public async Task LevelFilter_DrawsOnlyThatLevel()
    {
        var client = await factory.SignedInClient();
        var bank = QuestionBank.From(Content.ReadSeed(Content.SeedFolder));
        var game = await Start(client, "C2");
        Assert.Equal(Math.Min(60, bank.Count("C2")), game.Questions.Count);

        var unknown = await client.PostAsJsonAsync("/api/game/start", new { level = "Z9" });
        Assert.Equal(HttpStatusCode.BadRequest, unknown.StatusCode);
    }

    [Fact]
    public async Task Answers_BuildCombosAndFinishOnce()
    {
        var client = await factory.SignedInClient();
        var game = await Start(client);
        await Play(client, game.Id, true, true, true, false, true);

        var result = await Finish(client, game.Id);
        Assert.Equal(new GameResultDto(Game.ScoreOf(4, 3), 4, 5, 3, Game.ScoreOf(4, 3) / 10, Game.ScoreOf(4, 3), true), result);
        Assert.Equal(result, await Finish(client, game.Id));

        var points = await client.GetFromJsonAsync<PointsDto>("/api/points");
        Assert.Equal(result.PointsEarned, points!.Today);
        var late = await Answer(client, game.Id, 5, 0);
        Assert.Equal(HttpStatusCode.Conflict, late.StatusCode);
    }

    [Fact]
    public async Task Answers_MustFollowTheQuestionOrder()
    {
        var client = await factory.SignedInClient();
        var game = await Start(client);
        Assert.Equal(HttpStatusCode.Conflict, (await Answer(client, game.Id, 1, 0)).StatusCode);
        Assert.Equal(HttpStatusCode.BadRequest, (await Answer(client, game.Id, 0, 7)).StatusCode);
        Assert.Equal(HttpStatusCode.OK, (await Answer(client, game.Id, 0, 0)).StatusCode);
        Assert.Equal(HttpStatusCode.Conflict, (await Answer(client, game.Id, 0, 0)).StatusCode);
    }

    [Fact]
    public async Task AnswersAfterSixtySeconds_AreRejected()
    {
        var client = await factory.SignedInClient();
        var game = await Start(client);
        factory.Clock.Now += TimeSpan.FromSeconds(Game.DurationSeconds + 4);

        Assert.Equal(HttpStatusCode.Conflict, (await Answer(client, game.Id, 0, 0)).StatusCode);
        Assert.Equal(0, (await Finish(client, game.Id)).Answered);
    }

    [Fact]
    public async Task Games_BelongToTheirPlayer()
    {
        var game = await Start(await factory.SignedInClient());
        var other = await factory.SignedInClient();
        Assert.Equal(HttpStatusCode.NotFound, (await Answer(other, game.Id, 0, 0)).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound, (await other.PostAsync($"/api/game/{game.Id}/finish", null)).StatusCode);
    }

    [Fact]
    public async Task Records_KeepTheBestScore()
    {
        var client = await factory.SignedInClient();
        var first = await Start(client);
        await Play(client, first.Id, true, true);
        await Finish(client, first.Id);
        var second = await Start(client);
        await Play(client, second.Id, true);

        var result = await Finish(client, second.Id);
        Assert.False(result.IsRecord);
        Assert.Equal(Game.ScoreOf(2, 2), result.Best);
        Assert.Equal(new GameRecordsDto(Game.ScoreOf(2, 2), 2),
            await client.GetFromJsonAsync<GameRecordsDto>("/api/game/records"));
    }

    [Fact]
    public async Task GamePoints_ShareTheDailyCap()
    {
        var client = await factory.SignedInClient();
        var game = await Start(client);
        using (var scope = factory.Services.CreateScope())
        {
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var userId = await db.GameSessions.Where(s => s.Id == game.Id).Select(s => s.UserId).SingleAsync();
            db.PointLedger.Add(new PointEntry
            {
                UserId = userId, Source = "attempt", SourceId = "earlier", Points = Points.DailyCap - 2,
                LocalDate = Points.Today(factory.Clock.GetUtcNow()), CreatedAt = factory.Clock.GetUtcNow(),
            });
            await db.SaveChangesAsync();
        }
        await Play(client, game.Id, true, true, true);

        Assert.Equal(2, (await Finish(client, game.Id)).PointsEarned);
    }

    [Fact]
    public void QuestionBank_PutsTheMeaningAtTheAnswerIndex()
    {
        var bank = new QuestionBank([
            new("1", "apple", "quả táo", "A1"), new("2", "book", "quyển sách", "A1"),
            new("3", "cat", "con mèo", "A1"), new("4", "dog", "con chó", "A1"), new("5", "egg", "quả trứng", "B1"),
        ]);
        var questions = bank.Draw("A1", 10, new Random(7));
        Assert.Equal(4, questions.Count);
        var meanings = new Dictionary<string, string>
        {
            ["apple"] = "quả táo", ["book"] = "quyển sách", ["cat"] = "con mèo", ["dog"] = "con chó",
        };
        Assert.All(questions, q =>
        {
            Assert.Equal(meanings[q.Word], q.Options[q.Answer]);
            Assert.Equal(4, q.Options.Distinct().Count());
        });
    }

    [Fact]
    public void QuestionBank_TakesVisibleCompleteWordRows()
    {
        ContentItem Row(string id, string json, bool hidden = false) =>
            new() { Kind = "word", Id = id, Json = json, Hidden = hidden };
        var bank = QuestionBank.From([
            Row("1", """{"id":"1","word":"apple","meaning":"quả táo","level":"A1"}""", hidden: true),
            Row("2", """{"id":"2","word":"novel","meaning":"tiểu thuyết","level":"A1"}"""),
            Row("3", """{"id":"3","word":"odd","meaning":"lạ","level":"Z9"}"""),
            Row("4", """{"id":"4","word":""}"""),
            new ContentItem { Kind = "reading", Id = "r", Json = """{"id":"r","word":"x","meaning":"y","level":"A1"}""" },
        ]);
        Assert.Equal(["novel"], bank.Draw("A1", 10, new Random(1)).Select(q => q.Word));
    }
}
