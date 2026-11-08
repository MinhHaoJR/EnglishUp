using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace EnglishUp.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options)
    : IdentityDbContext<IdentityUser>(options)
{
    public DbSet<Attempt> Attempts => Set<Attempt>();
    public DbSet<SyncRecord> SyncRecords => Set<SyncRecord>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.Entity<Attempt>(entity =>
        {
            entity.HasKey(a => new { a.UserId, a.Id });
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(a => a.UserId);
            entity.Property(a => a.Id).HasMaxLength(128);
            entity.Property(a => a.Skill).HasMaxLength(16);
            entity.Property(a => a.Label).HasMaxLength(500);
            entity.Property(a => a.LearningLanguage).HasMaxLength(8);
            entity.HasIndex(a => new { a.UserId, a.Timestamp });
        });
        builder.Entity<SyncRecord>(entity =>
        {
            entity.HasKey(r => new { r.UserId, r.Store, r.Id });
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(r => r.UserId);
            entity.Property(r => r.Store).HasMaxLength(32);
            entity.Property(r => r.Id).HasMaxLength(128);
        });
    }
}

/// <summary>One saved practice result; typed so points and leaderboards can query it.</summary>
public class Attempt
{
    public required string UserId { get; set; }
    public required string Id { get; set; }
    public required string Skill { get; set; }
    public double Score { get; set; }
    public double Duration { get; set; }
    public double Timestamp { get; set; }
    public required string Label { get; set; }
    public string? LearningLanguage { get; set; }
}

/// <summary>A Dexie record (settings, words, reviews, drafts, submissions, vocabularyStudy) kept as JSON.</summary>
public class SyncRecord
{
    public required string UserId { get; set; }
    public required string Store { get; set; }
    public required string Id { get; set; }
    public double Version { get; set; }
    public required string Data { get; set; }
}
