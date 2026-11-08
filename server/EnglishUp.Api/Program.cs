using System.Text.Json.Serialization;
using EnglishUp.Api;
using EnglishUp.Api.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddAuthorization();
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

// The React app reaches these through the Vite /api proxy, so no CORS policy is needed.
var api = app.MapGroup("/api");
api.MapIdentityApi<IdentityUser>();
api.MapSync();
api.MapPoints();
api.MapGet("/health", () => Results.Ok(new { status = "ok" }));

app.Run();

public partial class Program;
