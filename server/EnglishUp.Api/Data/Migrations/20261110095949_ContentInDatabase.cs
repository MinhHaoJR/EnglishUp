using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace EnglishUp.Api.Data.Migrations
{
    /// <inheritdoc />
    public partial class ContentInDatabase : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // Rows without JSON only hid a bundled item; every item now has its JSON (the seed adds it back, visible).
            migrationBuilder.Sql("DELETE FROM \"ContentItems\" WHERE \"Json\" IS NULL;");

            migrationBuilder.AlterColumn<string>(
                name: "Json",
                table: "ContentItems",
                type: "text",
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "text",
                oldNullable: true);

            migrationBuilder.AddColumn<int>(
                name: "Position",
                table: "ContentItems",
                type: "integer",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Position",
                table: "ContentItems");

            migrationBuilder.AlterColumn<string>(
                name: "Json",
                table: "ContentItems",
                type: "text",
                nullable: true,
                oldClrType: typeof(string),
                oldType: "text");
        }
    }
}
