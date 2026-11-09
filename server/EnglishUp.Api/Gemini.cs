using System.Net;

namespace EnglishUp.Api;

/// <summary>A free-tier daily limit is used up; waiting minutes will not help.</summary>
public class DailyQuotaException()
    : HttpRequestException("Gemini daily quota used up", null, HttpStatusCode.TooManyRequests);

/// <summary>Shared Gemini REST call; the key comes from user-secrets or the environment, never the client.</summary>
public static class Gemini
{
    public static async Task<T> PostAsync<T>(HttpClient http, IConfiguration config, string model, string method,
        object body, CancellationToken ct)
    {
        var key = config["Gemini:ApiKey"];
        if (string.IsNullOrEmpty(key))
            throw new InvalidOperationException("Set Gemini:ApiKey with dotnet user-secrets: see README.");
        using var request = new HttpRequestMessage(HttpMethod.Post,
            $"https://generativelanguage.googleapis.com/v1beta/models/{model}:{method}")
        {
            Content = JsonContent.Create(body),
        };
        request.Headers.Add("x-goog-api-key", key);
        using var response = await http.SendAsync(request, ct);
        if (response.StatusCode == HttpStatusCode.TooManyRequests
            && (await response.Content.ReadAsStringAsync(ct)).Contains("PerDay"))
            throw new DailyQuotaException();
        if (!response.IsSuccessStatusCode)
            throw new HttpRequestException($"Gemini {method} failed: {(int)response.StatusCode}", null, response.StatusCode);
        return (await response.Content.ReadFromJsonAsync<T>(ct))!;
    }

    public const int MaxTries = 5;

    /// <summary>
    /// Waits out the free tier's per-minute limit (default 61 s) and retries, up to <see cref="MaxTries"/> calls;
    /// the daily limit and other errors are thrown at once.
    /// </summary>
    public static async Task<T> WithRetryAsync<T>(Func<Task<T>> call, TimeSpan? retryAfter, Action<string>? log,
        CancellationToken ct)
    {
        for (var tries = 1; ; tries++)
        {
            try
            {
                return await call();
            }
            catch (HttpRequestException e) when (e is not DailyQuotaException
                && e.StatusCode == HttpStatusCode.TooManyRequests && tries < MaxTries)
            {
                log?.Invoke("Rate limited; waiting a minute");
                await Task.Delay(retryAfter ?? TimeSpan.FromSeconds(61), ct);
            }
        }
    }

    /// <summary>503 with a reason the learner can act on.</summary>
    public static IResult Unavailable(HttpRequestException e) => Results.Problem(e switch
    {
        DailyQuotaException => "Today's AI quota is used up; try again tomorrow.",
        { StatusCode: HttpStatusCode.TooManyRequests } => "The AI quota is used up for now; try again in a minute.",
        _ => "The AI service is unavailable.",
    }, statusCode: StatusCodes.Status503ServiceUnavailable);
}
