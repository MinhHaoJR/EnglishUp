using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Pgvector;

namespace EnglishUp.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options)
    : IdentityDbContext<IdentityUser>(options)
{
    public DbSet<Attempt> Attempts => Set<Attempt>();
    public DbSet<SyncRecord> SyncRecords => Set<SyncRecord>();
    public DbSet<PointEntry> PointLedger => Set<PointEntry>();
    public DbSet<LearnerProfile> LearnerProfiles => Set<LearnerProfile>();
    public DbSet<UserAchievement> UserAchievements => Set<UserAchievement>();
    public DbSet<GameSession> GameSessions => Set<GameSession>();
    public DbSet<KnowledgeChunk> KnowledgeChunks => Set<KnowledgeChunk>();
    public DbSet<Conversation> Conversations => Set<Conversation>();
    public DbSet<ChatMessage> ChatMessages => Set<ChatMessage>();
    public DbSet<MessageCitation> MessageCitations => Set<MessageCitation>();
    public DbSet<Presence> Presence => Set<Presence>();
    public DbSet<ContentItem> ContentItems => Set<ContentItem>();

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
        builder.Entity<PointEntry>(entity =>
        {
            entity.ToTable("PointLedger");
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(p => p.UserId);
            entity.Property(p => p.Source).HasMaxLength(16);
            entity.Property(p => p.SourceId).HasMaxLength(128);
            // One award per source, however often a device re-sends it.
            entity.HasIndex(p => new { p.UserId, p.Source, p.SourceId }).IsUnique();
            entity.HasIndex(p => new { p.UserId, p.LocalDate });
        });
        builder.Entity<ContentItem>(entity =>
        {
            entity.HasKey(c => new { c.Kind, c.Id });
            entity.Property(c => c.Kind).HasMaxLength(16);
            entity.Property(c => c.Id).HasMaxLength(64);
            entity.Property(c => c.UpdatedBy).HasMaxLength(256);
        });
        builder.Entity<Presence>(entity =>
        {
            entity.HasKey(p => p.UserId);
            entity.HasOne<IdentityUser>().WithOne().HasForeignKey<Presence>(p => p.UserId);
            entity.HasIndex(p => p.LastSeenAt);
        });
        builder.Entity<LearnerProfile>(entity =>
        {
            entity.HasKey(p => p.UserId);
            entity.HasOne<IdentityUser>().WithOne().HasForeignKey<LearnerProfile>(p => p.UserId);
            entity.Property(p => p.DisplayName).HasMaxLength(40);
        });
        builder.Entity<UserAchievement>(entity =>
        {
            entity.HasKey(a => new { a.UserId, a.Code });
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(a => a.UserId);
            entity.Property(a => a.Code).HasMaxLength(32);
        });
        builder.Entity<GameSession>(entity =>
        {
            entity.Property(g => g.Mode).HasMaxLength(16);
            entity.HasIndex(g => new { g.Mode, g.StartedAt });
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(g => g.UserId);
            entity.Property(g => g.Level).HasMaxLength(8);
            // Two answers to the same question must not both count.
            entity.Property(g => g.Answered).IsConcurrencyToken();
            entity.HasIndex(g => new { g.UserId, g.StartedAt });
        });
        builder.HasPostgresExtension("vector");
        builder.Entity<KnowledgeChunk>(entity =>
        {
            entity.Property(c => c.SourceType).HasMaxLength(16);
            entity.Property(c => c.SourceId).HasMaxLength(128);
            entity.Property(c => c.Title).HasMaxLength(200);
            entity.Property(c => c.Text).HasMaxLength(4000);
            entity.Property(c => c.ContentHash).HasMaxLength(64).IsFixedLength();
            entity.Property(c => c.EmbeddingModel).HasMaxLength(64);
            entity.Property(c => c.Embedding).HasColumnType($"vector({EnglishUp.Api.GeminiEmbedder.Dimensions})");
            entity.HasIndex(c => new { c.SourceType, c.SourceId }).IsUnique();
            entity.HasIndex(c => c.Embedding).HasMethod("hnsw").HasOperators("vector_cosine_ops");
            // The in-memory test database has no vector type; store the floats as JSON instead.
            if (!Database.IsNpgsql())
                entity.Property(c => c.Embedding).HasConversion(
                    v => System.Text.Json.JsonSerializer.Serialize(v.ToArray(), (System.Text.Json.JsonSerializerOptions?)null),
                    s => new Vector(System.Text.Json.JsonSerializer.Deserialize<float[]>(s, (System.Text.Json.JsonSerializerOptions?)null)!));
        });
        builder.Entity<Conversation>(entity =>
        {
            entity.HasOne<IdentityUser>().WithMany().HasForeignKey(c => c.UserId);
            entity.HasIndex(c => new { c.UserId, c.CreatedAt });
        });
        builder.Entity<ChatMessage>(entity =>
        {
            entity.HasOne<Conversation>().WithMany().HasForeignKey(m => m.ConversationId);
            entity.Property(m => m.Role).HasMaxLength(16);
            entity.Property(m => m.Content).HasMaxLength(4000);
            entity.HasIndex(m => new { m.ConversationId, m.Id });
        });
        builder.Entity<MessageCitation>(entity =>
        {
            entity.HasKey(c => new { c.MessageId, c.ChunkId });
            entity.HasOne<ChatMessage>().WithMany().HasForeignKey(c => c.MessageId);
            // Ingest deletes chunks that left the content; their citations go with them.
            entity.HasOne<KnowledgeChunk>().WithMany().HasForeignKey(c => c.ChunkId);
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

/// <summary>One award of points; totals and leaderboards are sums over this ledger.</summary>
public class PointEntry
{
    public long Id { get; set; }
    public required string UserId { get; set; }
    public required string Source { get; set; }
    public required string SourceId { get; set; }
    public int Points { get; set; }
    public DateOnly LocalDate { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
}

/// <summary>Public face of a learner; hidden from the leaderboard until they opt in.</summary>
/// <summary>An admin's addition, edit or hiding of one learning item; see Content.cs.</summary>
public class ContentItem
{
    public required string Kind { get; set; }
    public required string Id { get; set; }
    /// <summary>The item as JSON in the client's schema.</summary>
    public required string Json { get; set; }
    /// <summary>Order within the kind, as the app lists it (seed file order, new items last).</summary>
    public int Position { get; set; }
    public bool Hidden { get; set; }
    public DateTimeOffset UpdatedAt { get; set; }
    public string UpdatedBy { get; set; } = "";
}

/// <summary>When the learner last had the app open (a heartbeat every minute); see Admin.cs.</summary>
public class Presence
{
    public required string UserId { get; set; }
    public DateTimeOffset LastSeenAt { get; set; }
}

public class LearnerProfile
{
    public required string UserId { get; set; }
    public required string DisplayName { get; set; }
    public bool ShowOnLeaderboard { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
}

/// <summary>A badge a learner has earned; the rules are in Community.cs.</summary>
public class UserAchievement
{
    public required string UserId { get; set; }
    public required string Code { get; set; }
    public DateTimeOffset EarnedAt { get; set; }
}

/// <summary>One 60-second quiz game; questions and answers stay on the server.</summary>
public class GameSession
{
    public Guid Id { get; set; }
    public required string UserId { get; set; }
    public string? Level { get; set; }
    /// <summary><c>vocabulary</c> (meanings) or <c>grammar</c> (fill the blank); each has its own records and leaderboard.</summary>
    public string Mode { get; set; } = Game.Vocabulary;
    public required string QuestionsJson { get; set; }
    public DateTimeOffset StartedAt { get; set; }
    public DateTimeOffset? FinishedAt { get; set; }
    public int Answered { get; set; }
    public int Correct { get; set; }
    public int Combo { get; set; }
    public int MaxCombo { get; set; }
    public int? Score { get; set; }
}

/// <summary>One embedded piece of the app's learning content, searched by the RAG assistant.</summary>
public class KnowledgeChunk
{
    public int Id { get; set; }
    public required string SourceType { get; set; }
    public required string SourceId { get; set; }
    public required string Title { get; set; }
    public required string Text { get; set; }
    /// <summary>SHA-256 of title and text; unchanged content is not embedded again.</summary>
    public required string ContentHash { get; set; }
    public required string EmbeddingModel { get; set; }
    public required Vector Embedding { get; set; }
}

/// <summary>One chat with the assistant; its title is the first question.</summary>
public class Conversation
{
    public Guid Id { get; set; }
    public required string UserId { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
    /// <summary>Set when the learner deletes it; the message text is erased, the rows stay for the daily limit.</summary>
    public DateTimeOffset? DeletedAt { get; set; }
}

/// <summary>A learner question ("user") or an assistant answer ("assistant").</summary>
public class ChatMessage
{
    public long Id { get; set; }
    public Guid ConversationId { get; set; }
    public required string Role { get; set; }
    public required string Content { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
}

/// <summary>A source an answer cites; Rank is the [n] used in the answer, Score the cosine similarity.</summary>
public class MessageCitation
{
    public long MessageId { get; set; }
    public int ChunkId { get; set; }
    public int Rank { get; set; }
    public double Score { get; set; }
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
