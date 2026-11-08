using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace EnglishUp.Api.Tests;

public class ApiFactory : WebApplicationFactory<Program>
{
    private readonly string database = Guid.NewGuid().ToString();

    /// <summary>The app's clock; tests move it forward to pass time limits.</summary>
    public ManualClock Clock { get; } = new(DateTimeOffset.UtcNow);

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");
        builder.ConfigureServices(services =>
        {
            // EF Core 9 keeps provider setup in IDbContextOptionsConfiguration; drop it with the options.
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.RemoveAll<IDbContextOptionsConfiguration<AppDbContext>>();
            services.AddDbContext<AppDbContext>(options => options.UseInMemoryDatabase(database));
            services.RemoveAll<TimeProvider>();
            services.AddSingleton<TimeProvider>(Clock);
            // Never call Gemini from tests.
            services.RemoveAll<IEmbedder>();
            services.AddSingleton<IEmbedder>(new FakeEmbedder());
        });
    }

    private record Tokens(string AccessToken);

    /// <summary>A client for a freshly registered learner.</summary>
    public async Task<HttpClient> SignedInClient()
    {
        var client = CreateClient();
        var credentials = new { email = $"learner-{Guid.NewGuid():N}@example.test", password = "Learn#2026" };
        (await client.PostAsJsonAsync("/api/register", credentials)).EnsureSuccessStatusCode();
        var tokens = await (await client.PostAsJsonAsync("/api/login", credentials)).Content.ReadFromJsonAsync<Tokens>();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", tokens!.AccessToken);
        return client;
    }
}

public class ManualClock(DateTimeOffset now) : TimeProvider
{
    public DateTimeOffset Now { get; set; } = now;
    public override DateTimeOffset GetUtcNow() => Now;
}

public class AuthTests(ApiFactory factory) : IClassFixture<ApiFactory>
{
    private const string Password = "Learn#2026";
    private readonly HttpClient client = factory.CreateClient();

    private record Tokens(string AccessToken, string RefreshToken, int ExpiresIn);

    private static string NewEmail() => $"learner-{Guid.NewGuid():N}@example.test";

    private Task<HttpResponseMessage> Register(string email, string password = Password) =>
        client.PostAsJsonAsync("/api/register", new { email, password });

    private Task<HttpResponseMessage> Login(string email, string password = Password) =>
        client.PostAsJsonAsync("/api/login", new { email, password });

    [Fact]
    public async Task Health_IsPublic()
    {
        var response = await client.GetAsync("/api/health");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task RegisteredLearner_CanLogInAndReadAccount()
    {
        var email = NewEmail();
        Assert.Equal(HttpStatusCode.OK, (await Register(email)).StatusCode);

        var login = await Login(email);
        Assert.Equal(HttpStatusCode.OK, login.StatusCode);
        var tokens = await login.Content.ReadFromJsonAsync<Tokens>();
        Assert.False(string.IsNullOrEmpty(tokens?.AccessToken));
        Assert.False(string.IsNullOrEmpty(tokens?.RefreshToken));

        using var request = new HttpRequestMessage(HttpMethod.Get, "/api/manage/info");
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", tokens!.AccessToken);
        var info = await client.SendAsync(request);
        Assert.Equal(HttpStatusCode.OK, info.StatusCode);
        Assert.Contains(email, await info.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task RefreshToken_IssuesNewAccessToken()
    {
        var email = NewEmail();
        await Register(email);
        var tokens = await (await Login(email)).Content.ReadFromJsonAsync<Tokens>();

        var refresh = await client.PostAsJsonAsync("/api/refresh", new { refreshToken = tokens!.RefreshToken });
        Assert.Equal(HttpStatusCode.OK, refresh.StatusCode);
        Assert.False(string.IsNullOrEmpty((await refresh.Content.ReadFromJsonAsync<Tokens>())?.AccessToken));
    }

    [Fact]
    public async Task AccountInfo_RequiresToken()
    {
        var response = await client.GetAsync("/api/manage/info");
        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task WrongPassword_IsRejected()
    {
        var email = NewEmail();
        await Register(email);
        Assert.Equal(HttpStatusCode.Unauthorized, (await Login(email, "Wrong#2026")).StatusCode);
    }

    [Fact]
    public async Task DuplicateEmail_IsRejected()
    {
        var email = NewEmail();
        await Register(email);
        Assert.Equal(HttpStatusCode.BadRequest, (await Register(email)).StatusCode);
    }

    [Theory]
    [InlineData("Ab#1")]
    [InlineData("alllowercase#1")]
    [InlineData("NoDigits#Here")]
    public async Task WeakPassword_IsRejected(string password)
    {
        Assert.Equal(HttpStatusCode.BadRequest, (await Register(NewEmail(), password)).StatusCode);
    }
}
