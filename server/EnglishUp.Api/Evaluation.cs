using System.Globalization;
using System.Text;
using System.Text.Json;
using EnglishUp.Api.Data;

namespace EnglishUp.Api;

/// <summary>One evaluation question; Expected holds "sourceType/sourceId" keys, empty when the lessons do not cover it.</summary>
public record EvalQuestion(string Id, string Question, string[] Expected);

/// <summary>Rank of the first expected source among the retrieved ones (1-based, null if missing).</summary>
public record EvalResult(EvalQuestion Item, int? Rank, double TopScore, bool CitedExpected, int Cited, string Answer);

/// <summary>
/// Offline evaluation of the assistant on a fixed question set: retrieval hit@1, hit@5 and MRR, and whether the answer
/// cites an expected source (or, for uncovered questions, cites nothing).
/// </summary>
public static class Evaluation
{
    public static List<EvalQuestion> Load(string path) =>
        JsonSerializer.Deserialize<List<EvalQuestion>>(File.ReadAllText(path), JsonSerializerOptions.Web)!;

    public static async Task<List<EvalResult>> RunAsync(AppDbContext db, IEmbedder embedder, IAnswerer answerer,
        IReadOnlyList<EvalQuestion> items, Action<string>? log = null, TimeSpan? retryAfter = null, CancellationToken ct = default)
    {
        var results = new List<EvalResult>();
        foreach (var item in items)
        {
            // The same path as POST /api/assistant/ask, without saving a conversation.
            var hits = await Gemini.WithRetryAsync(
                () => Knowledge.SearchAsync(db, embedder, item.Question, Assistant.SourceCount, ct), retryAfter, log, ct);
            var answer = await Gemini.WithRetryAsync(() => answerer.AnswerAsync(Assistant.SystemPrompt,
                [new ChatTurn("user", Assistant.SourcesPrompt(hits, item.Question))], ct), retryAfter, log, ct);
            var keys = hits.Select(h => $"{h.SourceType}/{h.SourceId}").ToList();
            var rank = keys.FindIndex(item.Expected.Contains) is var i and >= 0 ? i + 1 : (int?)null;
            var cited = Assistant.CitedNumbers(answer, hits.Count);
            var citedExpected = item.Expected.Length == 0
                ? cited.Count == 0
                : cited.Any(n => item.Expected.Contains(keys[n - 1]));
            results.Add(new EvalResult(item, rank, hits.Count > 0 ? hits[0].Score : 0, citedExpected, cited.Count, answer));
            log?.Invoke($"{item.Id}: rank {rank?.ToString() ?? "-"}, cited ok {citedExpected}");
        }
        return results;
    }

    /// <summary>A Markdown report with the summary and one row per question.</summary>
    public static string Report(IReadOnlyList<EvalResult> results, string model, DateTimeOffset when)
    {
        var answerable = results.Where(r => r.Item.Expected.Length > 0).ToList();
        var uncovered = results.Where(r => r.Item.Expected.Length == 0).ToList();
        string Pct(int n, int of) => of == 0 ? "-" : $"{n}/{of} ({100.0 * n / of:0}%)";
        var mrr = answerable.Count == 0 ? 0 : answerable.Sum(r => r.Rank is { } k ? 1.0 / k : 0) / answerable.Count;

        var text = new StringBuilder();
        text.AppendLine($"# Assistant evaluation, {when:yyyy-MM-dd HH:mm} UTC");
        text.AppendLine();
        text.AppendLine($"Answer model `{model}`, {Assistant.SourceCount} sources per question, {results.Count} questions.");
        text.AppendLine();
        text.AppendLine("| Metric | Result |");
        text.AppendLine("| --- | --- |");
        text.AppendLine($"| Retrieval hit@1 | {Pct(answerable.Count(r => r.Rank == 1), answerable.Count)} |");
        text.AppendLine($"| Retrieval hit@5 | {Pct(answerable.Count(r => r.Rank is not null), answerable.Count)} |");
        text.AppendLine($"| Retrieval MRR | {mrr.ToString("0.00", CultureInfo.InvariantCulture)} |");
        text.AppendLine($"| Answer cites an expected source | {Pct(answerable.Count(r => r.CitedExpected), answerable.Count)} |");
        text.AppendLine($"| Uncovered question answered without citations | {Pct(uncovered.Count(r => r.CitedExpected), uncovered.Count)} |");
        text.AppendLine();
        text.AppendLine("| Id | Question | Expected | Rank | Top score | Citations ok | Answer |");
        text.AppendLine("| --- | --- | --- | --- | --- | --- | --- |");
        foreach (var r in results)
            text.AppendLine($"| {r.Item.Id} | {Cell(r.Item.Question)} | {(r.Item.Expected.Length == 0 ? "none" : string.Join(", ", r.Item.Expected))} " +
                $"| {r.Rank?.ToString() ?? "-"} | {r.TopScore.ToString("0.00", CultureInfo.InvariantCulture)} | {(r.CitedExpected ? "yes" : "no")} | {Cell(r.Answer)} |");
        return text.ToString();
    }

    private static string Cell(string text) => text.ReplaceLineEndings(" ").Replace("|", "\\|");
}
