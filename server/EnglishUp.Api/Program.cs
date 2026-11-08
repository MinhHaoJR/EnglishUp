using System.Text.Json.Serialization;
using EnglishUp.Api;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default"), npgsql => npgsql.UseVector()));
builder.Services.AddAuthorization();
builder.Services.AddSingleton(TimeProvider.System);
var content = Path.Combine(AppContext.BaseDirectory, "Content");
builder.Services.AddSingleton(QuestionBank.Load(content));
builder.Services.AddHttpClient<IEmbedder, GeminiEmbedder>();
// Optional fields (e.g. an attempt without learningLanguage) stay absent, matching the client schemas.
builder.Services.ConfigureHttpJsonOptions(options =>
    options.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull);
builder.Services
    .AddIdentityApiEndpoints<IdentityUser>(options =>
    {
        options.User.RequireUniqueEmail = true;
        options.Password.RequiredLength = 8;
    })
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

// `dotnet run --project EnglishUp.Api -- ingest` embeds the learning content for the assistant, then exits.
if (args.Contains("ingest"))
{
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    try
    {
        var report = await Knowledge.IngestAsync(db, scope.ServiceProvider.GetRequiredService<IEmbedder>(),
            Knowledge.BuildChunks(content), Console.WriteLine);
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

// The React app reaches these through the Vite /api proxy, so no CORS policy is needed.
var api = app.MapGroup("/api");
api.MapIdentityApi<IdentityUser>();
api.MapSync();
api.MapPoints();
api.MapCommunity();
api.MapGame();
api.MapKnowledge();
api.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();

public partial class Program;
