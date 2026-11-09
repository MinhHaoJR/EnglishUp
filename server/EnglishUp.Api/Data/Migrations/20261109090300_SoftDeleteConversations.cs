using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EnglishUp.Api.Data.Migrations
{
    /// <inheritdoc />
    public partial class SoftDeleteConversations : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateTimeOffset>(
                name: "DeletedAt",
                table: "Conversations",
                type: "timestamp with time zone",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "DeletedAt",
                table: "Conversations");
        }
    }
}
