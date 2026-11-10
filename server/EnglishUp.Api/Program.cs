using System.Text.Json.Serialization;
using EnglishUp.Api;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default"), npgsql => npgsql.UseVector()));
builder.Services.AddAuthorizationBuilder().AddPolicy(Admin.Policy, policy => policy.RequireRole(Admin.Role));
builder.Services.AddSingleton(TimeProvider.System);
var content = Path.Combine(AppContext.BaseDirectory, "Content");
builder.Services.AddSingleton(QuestionBank.Load(content));
builder.Services.AddHttpClient<IEmbedder, GeminiEmbedder>();
builder.Services.AddHttpClient<IAnswerer, GeminiAnswerer>();
// Optional fields (e.g. an attempt without learningLanguage) stay absent, matching the client schemas.
builder.Services.ConfigureHttpJsonOptions(options =>
    options.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull);
builder.Services
    .AddIdentityApiEndpoints<IdentityUser>(options =>
    {
        options.User.RequireUniqueEmail = true;
        options.Password.RequiredLength = 8;
    })
    .AddRoles<IdentityRole>()
    .AddEntityFrameworkStores<AppDbContext>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    if (string.IsNullOrEmpty(app.Configuration.GetConnectionString("Default")))
        throw new InvalidOperationException(
            "Set ConnectionStrings:Default to your Supabase session pooler: see README, 'Optional account server'.");
    using var scope = app.Services.CreateScope();
    scope.ServiceProvider.GetRequiredService<AppDbContext>().Database.Migrate();
}

// `dotnet run --project EnglishUp.Api -- ingest [max]` embeds the learning content for the assistant, then exits.
// A max keeps part of the free daily quota (1,000 embeddings) for learners' searches.
if (args.Contains("ingest"))
{
    int? max = int.TryParse(args.SkipWhile(a => a != "ingest").Skip(1).FirstOrDefault(), out var limit) ? limit : null;
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    try
    {
        var report = await Knowledge.IngestAsync(db, scope.ServiceProvider.GetRequiredService<IEmbedder>(),
            Knowledge.BuildChunks(content), Console.WriteLine, max: max);
        Console.WriteLine($"Ingest done: {report}");
    }
    catch (DailyQuotaException)
    {
        Console.WriteLine($"Gemini's free daily quota is used up with {await db.KnowledgeChunks.CountAsync()} chunks saved. " +
            "Run ingest again after it resets (about 15:00 Vietnam time).");
        Environment.ExitCode = 1;
    }
    return;
}

// `dotnet run --project EnglishUp.Api -- eval <questions.json> [report.md]` runs the assistant evaluation, then exits.
// Each question uses one embedding and one answer from the free Gemini quota.
if (args.Contains("eval"))
{
    var paths = args.SkipWhile(a => a != "eval").Skip(1).ToArray();
    using var scope = app.Services.CreateScope();
    var answerer = scope.ServiceProvider.GetRequiredService<IAnswerer>();
    var results = await Evaluation.RunAsync(scope.ServiceProvider.GetRequiredService<AppDbContext>(),
        scope.ServiceProvider.GetRequiredService<IEmbedder>(), answerer, Evaluation.Load(paths[0]), Console.WriteLine);
    var report = Evaluation.Report(results, (answerer as GeminiAnswerer)?.Model ?? "unknown", DateTimeOffset.UtcNow);
    if (paths.Length > 1) File.WriteAllText(paths[1], report);
    else Console.WriteLine(report);
    return;
}

// `dotnet run --project EnglishUp.Api -- demo [remove]` adds (or removes) labelled demo learners for the
// leaderboard, then exits. They have no password, so nobody can sign in as them.
if (args.Contains("demo"))
{
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    if (args.Contains("remove"))
        Console.WriteLine($"Removed {await Demo.RemoveAsync(db)} demo learners.");
    else
        Console.WriteLine($"Added {await Demo.SeedAsync(db,
            scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>(), DateTimeOffset.UtcNow)} " +
            "demo learners. Remove them with: demo remove");
    return;
}

// `dotnet run --project EnglishUp.Api -- admin <email> [--remove]` puts an existing account in the Admin
// role (or takes it out), then exits. The learner signs out and in again to get a token with the change.
if (args.Contains("admin"))
{
    var email = args.SkipWhile(a => a != "admin").Skip(1).FirstOrDefault(a => !a.StartsWith("--"));
    var remove = args.Contains("--remove");
    using var scope = app.Services.CreateScope();
    var users = scope.ServiceProvider.GetRequiredService<UserManager<IdentityUser>>();
    var done = email is not null && (remove
        ? await Admin.RevokeAsync(users, email)
        : await Admin.GrantAsync(users, scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>(), email));
    Console.WriteLine(!done
        ? "Usage: admin <email of an existing account> [--remove]. No account has that email."
        : remove
            ? $"{email} is no longer an admin."
            : $"{email} is now an admin. Sign out and in again to open /admin.");
    Environment.ExitCode = done ? 0 : 1;
    return;
}

// The React app reaches these through the Vite /api proxy, so no CORS policy is needed.
var api = app.MapGroup("/api");
api.MapIdentityApi<IdentityUser>();
api.MapSync();
api.MapPoints();
api.MapCommunity();
api.MapGame();
api.MapKnowledge();
api.MapAssistant();
api.MapAdmin();
api.MapContent();
api.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();

public partial class Program;
