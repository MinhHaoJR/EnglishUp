using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EnglishUp.Api.Data.Migrations
{
    /// <inheritdoc />
    public partial class GameModes : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Mode",
                table: "GameSessions",
                type: "character varying(16)",
                maxLength: 16,
                nullable: false,
                // Every game before this migration was a vocabulary race.
                defaultValue: "vocabulary");

            migrationBuilder.CreateIndex(
                name: "IX_GameSessions_Mode_StartedAt",
                table: "GameSessions",
                columns: new[] { "Mode", "StartedAt" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_GameSessions_Mode_StartedAt",
                table: "GameSessions");

            migrationBuilder.DropColumn(
                name: "Mode",
                table: "GameSessions");
        }
    }
}
