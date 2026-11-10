using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.DependencyInjection;

namespace EnglishUp.Api.Tests;

public class AdminTests
{
    private const string Password = "Learn#2026";
    private record Tokens(string AccessToken);

    /// <summary>A fresh database per test, so counts are exact.</summary>
    private static async Task<(ApiFactory factory, HttpClient admin)> Setup()
    {
        var factory = new ApiFactory();
        return (factory, await Learner(factory, admin: true));
    }

    private static async Task<HttpClient> Learner(ApiFactory factory, bool admin = false, string? email = null)
    {
        var client = factory.CreateClient();
        email ??= $"learner-{Guid.NewGuid():N}@example.test";
        (await client.PostAsJsonAsync("/api/register", new { email, password = Password })).EnsureSuccessStatusCode();
        if (admin)
        {
            using var scope = factory.Services.CreateScope();
            Assert.True(await Admin.GrantAsync(
                scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>(),
                scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>(), email));
        }
        // Signing in after the grant puts the role in the token.
        var tokens = await (await client.PostAsJsonAsync("/api/login", new { email, password = Password }))
            .Content.ReadFromJsonAsync<Tokens>();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", tokens!.AccessToken);
        return client;
    }

    [Fact]
    public async Task AdminArea_IsForAdminsOnly()
    {
        var (factory, admin) = await Setup();
        using var _ = factory;
        var learner = await Learner(factory);

        Assert.Equal(HttpStatusCode.Unauthorized, (await factory.CreateClient().GetAsync("/api/admin/overview")).StatusCode);
        Assert.Equal(HttpStatusCode.Forbidden, (await learner.GetAsync("/api/admin/overview")).StatusCode);
        Assert.Equal(HttpStatusCode.Forbidden, (await learner.GetAsync("/api/admin/users")).StatusCode);
        Assert.Equal(HttpStatusCode.OK, (await admin.GetAsync("/api/admin/overview")).StatusCode);

        Assert.False((await learner.GetFromJsonAsync<MeDto>("/api/me"))!.IsAdmin);
        Assert.True((await admin.GetFromJsonAsync<MeDto>("/api/me"))!.IsAdmin);
    }

    [Fact]
    public async Task Heartbeats_SplitUsersIntoOnlineAndOffline()
    {
        var (factory, admin) = await Setup();
        using var _ = factory;
        var learner = await Learner(factory, email: "online@example.test");
        await Learner(factory, email: "never@example.test");

        Assert.Equal(HttpStatusCode.NoContent, (await learner.PostAsync("/api/presence", null)).StatusCode);
        Assert.Equal(HttpStatusCode.NoContent, (await learner.PostAsync("/api/presence", null)).StatusCode);
        var overview = await admin.GetFromJsonAsync<OverviewDto>("/api/admin/overview");
        Assert.Equal(3, overview!.Users);
        Assert.Equal(1, overview.Online);
        Assert.Equal(2, overview.Offline);

        var users = await admin.GetFromJsonAsync<List<AdminUserDto>>("/api/admin/users");
        Assert.Equal("online@example.test", users![0].Email); // most recently seen first
        Assert.True(users[0].Online);
        Assert.Null(users.Single(u => u.Email == "never@example.test").LastSeenAt);
        Assert.StartsWith("learner-", users.Single(u => u.IsAdmin).Email);

        // Three minutes without a heartbeat: offline, still listed with the time last seen.
        factory.Clock.Now += TimeSpan.FromMinutes(3);
        overview = await admin.GetFromJsonAsync<OverviewDto>("/api/admin/overview");
        Assert.Equal(0, overview!.Online);
        users = await admin.GetFromJsonAsync<List<AdminUserDto>>("/api/admin/users?search=ONLINE@");
        Assert.False(Assert.Single(users!).Online);
        Assert.NotNull(users![0].LastSeenAt);
    }

    [Fact]
    public async Task LockingAnAccount_StopsSignIn_AndAdminsCannotLockThemselves()
    {
        var (factory, admin) = await Setup();
        using var _ = factory;
        await Learner(factory, email: "locked@example.test");
        var users = await admin.GetFromJsonAsync<List<AdminUserDto>>("/api/admin/users");
        var target = users!.Single(u => u.Email == "locked@example.test");
        var self = users.Single(u => u.IsAdmin);

        Assert.Equal(HttpStatusCode.BadRequest,
            (await admin.PostAsJsonAsync($"/api/admin/users/{self.Id}/lock", new { locked = true })).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound,
            (await admin.PostAsJsonAsync("/api/admin/users/nobody/lock", new { locked = true })).StatusCode);

        Assert.Equal(HttpStatusCode.NoContent,
            (await admin.PostAsJsonAsync($"/api/admin/users/{target.Id}/lock", new { locked = true })).StatusCode);
        var anonymous = factory.CreateClient();
        Assert.Equal(HttpStatusCode.Unauthorized, (await anonymous.PostAsJsonAsync("/api/login",
            new { email = "locked@example.test", password = Password })).StatusCode);
        Assert.True((await admin.GetFromJsonAsync<List<AdminUserDto>>("/api/admin/users?search=locked"))![0].Locked);
        Assert.Equal(1, (await admin.GetFromJsonAsync<OverviewDto>("/api/admin/overview"))!.Locked);

        Assert.Equal(HttpStatusCode.NoContent,
            (await admin.PostAsJsonAsync($"/api/admin/users/{target.Id}/lock", new { locked = false })).StatusCode);
        Assert.Equal(HttpStatusCode.OK, (await anonymous.PostAsJsonAsync("/api/login",
            new { email = "locked@example.test", password = Password })).StatusCode);
    }

    [Fact]
    public async Task HidingALearner_TakesThemOffTheLeaderboard()
    {
        var (factory, admin) = await Setup();
        using var _ = factory;
        var learner = await Learner(factory, email: "rude@example.test");
        (await learner.PutAsJsonAsync("/api/profile", new { displayName = "Rude name", showOnLeaderboard = true }))
            .EnsureSuccessStatusCode();
        var id = (await admin.GetFromJsonAsync<List<AdminUserDto>>("/api/admin/users?search=rude name"))!.Single().Id;

        Assert.Equal(HttpStatusCode.NoContent, (await admin.PostAsync($"/api/admin/users/{id}/hide", null)).StatusCode);
        Assert.False((await learner.GetFromJsonAsync<ProfileDto>("/api/profile"))!.ShowOnLeaderboard);
    }

    [Fact]
    public async Task Revoke_TakesTheRoleAway()
    {
        var (factory, admin) = await Setup();
        using var _ = factory;
        var email = (await admin.GetFromJsonAsync<MeDto>("/api/me"))!.Email;
        using (var scope = factory.Services.CreateScope())
            Assert.True(await Admin.RevokeAsync(scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>(), email));
        Assert.False((await admin.GetFromJsonAsync<MeDto>("/api/me"))!.IsAdmin);
    }

    [Fact]
    public async Task Grant_FailsForUnknownEmail()
    {
        using var factory = new ApiFactory();
        using var scope = factory.Services.CreateScope();
        Assert.False(await Admin.GrantAsync(
            scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>(),
            scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>(), "nobody@example.test"));
    }
}
