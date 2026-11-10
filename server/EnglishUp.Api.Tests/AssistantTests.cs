using System.Net;
using System.Net.Http.Json;
using EnglishUp.Api.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

/// <summary>Returns a fixed answer and remembers what it was sent.</summary>
public class FakeAnswerer : IAnswerer
{
    public string Answer { get; set; } = "Routine nghĩa là thói quen hằng ngày [1]. Xem thêm [2][2][9].";
    public HttpStatusCode? Failure { get; set; }
    public IReadOnlyList<ChatTurn> LastTurns { get; private set; } = [];
    public string LastSystem { get; private set; } = "";

    public Task<string> AnswerAsync(string system, IReadOnlyList<ChatTurn> turns, CancellationToken ct = default)
    {
        if (Failure is { } status) throw new HttpRequestException("fake", null, status);
        (LastSystem, LastTurns) = (system, turns);
        return Task.FromResult(Answer);
    }
}

public class AssistantTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory factory;
    private FakeAnswerer Answerer => (FakeAnswerer)factory.Services.GetRequiredService<IAnswerer>();

    public AssistantTests(ApiFactory factory)
    {
        this.factory = factory;
        using var scope = factory.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        if (!db.KnowledgeChunks.Any())
            Knowledge.IngestAsync(db, scope.ServiceProvider.GetRequiredService<IEmbedder>(),
                Knowledge.BuildChunks(EnglishUp.Api.Content.ReadSeed(EnglishUp.Api.Content.SeedFolder))).GetAwaiter().GetResult();
    }

    private static async Task<AssistantReply> Ask(HttpClient client, string question, Guid? conversationId = null)
    {
        var response = await client.PostAsJsonAsync("/api/assistant/ask", new { conversationId, question });
        response.EnsureSuccessStatusCode();
        return (await response.Content.ReadFromJsonAsync<AssistantReply>())!;
    }

    [Fact]
    public async Task Evaluation_ScoresRetrievalAndCitations()
    {
        List<EvalQuestion> items =
        [
            new("a", "routine", ["word/v-1-1"]),
            new("b", "Mai Ben Saturday birthday gift bookshop", ["listening/l1"]),
            new("c", "capital of Australia", []),
        ];
        using var scope = factory.Services.CreateScope();
        var results = await Evaluation.RunAsync(scope.ServiceProvider.GetRequiredService<AppDbContext>(),
            scope.ServiceProvider.GetRequiredService<IEmbedder>(), Answerer, items);

        Assert.Equal([1, 1], results.Take(2).Select(r => r.Rank));
        Assert.All(results.Take(2), r => Assert.True(r.CitedExpected));
        Assert.False(results[2].CitedExpected); // the fake answer cites [1] even when nothing fits
        var report = Evaluation.Report(results, "fake", DateTimeOffset.UnixEpoch);
        Assert.Contains("| Retrieval hit@1 | 2/2 (100%) |", report);
        Assert.Contains("| Uncovered question answered without citations | 0/1 (0%) |", report);
        Assert.Contains("| c | capital of Australia | none | ", report);
    }

    [Fact]
    public void EvaluationSet_HasThirtyQuestionsWithKnownSources()
    {
        var items = Evaluation.Load(Path.Combine(AppContext.BaseDirectory, "eval", "assistant-questions.json"));
        Assert.Equal(30, items.Count);
        Assert.Equal(30, items.Select(i => i.Id).Distinct().Count());
        var known = Knowledge.BuildChunks(EnglishUp.Api.Content.ReadSeed(EnglishUp.Api.Content.SeedFolder))
            .Select(c => $"{c.SourceType}/{c.SourceId}").ToHashSet();
        Assert.All(items.SelectMany(i => i.Expected), key => Assert.Contains(key, known));
    }

    [Fact]
    public void StartOfToday_IsVietnamMidnightInUtc()
    {
        // 2026-11-09 01:30 in Vietnam is still 2026-11-08 in UTC.
        var start = Points.StartOfToday(new DateTimeOffset(2026, 11, 8, 18, 30, 0, TimeSpan.Zero));
        Assert.Equal(new DateTimeOffset(2026, 11, 8, 17, 0, 0, TimeSpan.Zero), start);
        Assert.Equal(TimeSpan.Zero, start.Offset); // Npgsql rejects other offsets for timestamptz
    }

    [Fact]
    public void CitedNumbers_KeepsValidSourcesInFirstUseOrder() =>
        Assert.Equal([3, 1], Assistant.CitedNumbers("a [3] b [1] c [3] d [0] e [6] f [12]", 5));

    [Fact]
    public async Task Assistant_RequiresTokenAndAValidQuestion()
    {
        Assert.Equal(HttpStatusCode.Unauthorized,
            (await factory.CreateClient().PostAsJsonAsync("/api/assistant/ask", new { question = "hi" })).StatusCode);
        var client = await factory.SignedInClient();
        foreach (var question in new[] { "", "   ", new string('a', Assistant.MaxQuestionLength + 1) })
            Assert.Equal(HttpStatusCode.BadRequest,
                (await client.PostAsJsonAsync("/api/assistant/ask", new { question })).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound,
            (await client.PostAsJsonAsync("/api/assistant/ask", new { conversationId = Guid.NewGuid(), question = "hi" })).StatusCode);
    }

    [Fact]
    public async Task Ask_AnswersFromRetrievedSourcesAndKeepsCitedOnes()
    {
        var client = await factory.SignedInClient();
        // The fake embedder matches words, so a one-word question makes the top source predictable.
        var reply = await Ask(client, "routine");

        Assert.Equal(Answerer.Answer, reply.Answer);
        Assert.Equal(Assistant.DailyQuestions - 1, reply.QuestionsLeft);
        Assert.Equal([1, 2], reply.Citations.Select(c => c.N));
        Assert.Equal(("word", "routine"), (reply.Citations[0].SourceType, reply.Citations[0].Title));
        Assert.Equal(Assistant.SystemPrompt, Answerer.LastSystem);
        var prompt = Assert.Single(Answerer.LastTurns);
        Assert.StartsWith("Sources:\n[1] (word) routine\n", prompt.Text);
        Assert.EndsWith("Question: routine", prompt.Text);
        Assert.Contains("[5] ", prompt.Text);
    }

    [Fact]
    public async Task FollowUps_SendTheHistoryAndAreListed()
    {
        var client = await factory.SignedInClient();
        var first = await Ask(client, "What does routine mean?");
        var second = await Ask(client, "Cho tôi một ví dụ", first.ConversationId);
        Assert.Equal(first.ConversationId, second.ConversationId);
        Assert.Equal(["user", "model", "user"], Answerer.LastTurns.Select(t => t.Role));
        Assert.Equal("What does routine mean?", Answerer.LastTurns[0].Text);
        Assert.Equal(first.Answer, Answerer.LastTurns[1].Text);

        var list = await client.GetFromJsonAsync<List<ConversationSummary>>("/api/assistant/conversations");
        Assert.Equal("What does routine mean?", Assert.Single(list!).Title);
        var messages = await client.GetFromJsonAsync<List<MessageDto>>($"/api/assistant/conversations/{first.ConversationId}");
        Assert.Equal(["user", "assistant", "user", "assistant"], messages!.Select(m => m.Role));
        Assert.Equal([1, 2], messages[1].Citations.Select(c => c.N));
        Assert.Empty(messages[0].Citations);
    }

    [Fact]
    public async Task Conversations_BelongToTheirLearnerAndCanBeDeleted()
    {
        var owner = await factory.SignedInClient();
        var id = (await Ask(owner, "What does routine mean?")).ConversationId;
        var other = await factory.SignedInClient();
        Assert.Equal(HttpStatusCode.NotFound, (await other.GetAsync($"/api/assistant/conversations/{id}")).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound, (await other.DeleteAsync($"/api/assistant/conversations/{id}")).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound,
            (await other.PostAsJsonAsync("/api/assistant/ask", new { conversationId = id, question = "hi" })).StatusCode);
        Assert.Empty((await other.GetFromJsonAsync<List<ConversationSummary>>("/api/assistant/conversations"))!);

        Assert.Equal(HttpStatusCode.NoContent, (await owner.DeleteAsync($"/api/assistant/conversations/{id}")).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound, (await owner.GetAsync($"/api/assistant/conversations/{id}")).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound, (await owner.DeleteAsync($"/api/assistant/conversations/{id}")).StatusCode);
        Assert.Empty((await owner.GetFromJsonAsync<List<ConversationSummary>>("/api/assistant/conversations"))!);
        using var scope = factory.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        Assert.All(await db.ChatMessages.Where(m => m.ConversationId == id).ToListAsync(), m => Assert.Equal("", m.Content));

        // Deleting does not give the questions back.
        Assert.Equal(Assistant.DailyQuestions - 2, (await Ask(owner, "Another question")).QuestionsLeft);
    }

    [Fact]
    public async Task DailyQuestionLimit_ResetsAtVietnamMidnight()
    {
        var client = await factory.SignedInClient();
        var reply = await Ask(client, "What does routine mean?");
        using (var scope = factory.Services.CreateScope())
        {
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.ChatMessages.AddRange(Enumerable.Range(0, Assistant.DailyQuestions - 1).Select(_ => new ChatMessage
            {
                ConversationId = reply.ConversationId, Role = "user", Content = "earlier", CreatedAt = factory.Clock.GetUtcNow(),
            }));
            await db.SaveChangesAsync();
        }
        var blocked = await client.PostAsJsonAsync("/api/assistant/ask", new { question = "One more?" });
        Assert.Equal(HttpStatusCode.TooManyRequests, blocked.StatusCode);

        // Moving the clock would expire the sign-in token, so move the earlier questions to just before midnight instead.
        using (var scope = factory.Services.CreateScope())
        {
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var yesterday = Points.StartOfToday(factory.Clock.GetUtcNow()).AddMinutes(-1);
            await db.ChatMessages.Where(m => m.ConversationId == reply.ConversationId)
                .ForEachAsync(m => m.CreatedAt = yesterday);
            await db.SaveChangesAsync();
        }
        Assert.Equal(Assistant.DailyQuestions - 1, (await Ask(client, "One more?")).QuestionsLeft);
    }

    [Fact]
    public async Task GeminiFailure_Returns503AndSavesNothing()
    {
        var client = await factory.SignedInClient();
        Answerer.Failure = HttpStatusCode.InternalServerError;
        try
        {
            var response = await client.PostAsJsonAsync("/api/assistant/ask", new { question = "What does routine mean?" });
            Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode);
        }
        finally
        {
            Answerer.Failure = null;
        }
        Assert.Empty((await client.GetFromJsonAsync<List<ConversationSummary>>("/api/assistant/conversations"))!);
    }
}
