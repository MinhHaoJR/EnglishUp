# EnglishUp

Vietnamese/English learning app with optional accounts. React 18, strict TypeScript, Vite, Tailwind, Zustand, Dexie on the client; ASP.NET Core 9 Web API, EF Core (Npgsql) and PostgreSQL on Supabase in `server/`. Practice works without signing in. Dexie stays the working store; signed-in learners merge it with PostgreSQL through `POST /api/sync` (`src/services/sync.ts`, `server/EnglishUp.Api/Sync.cs`).

## Structure

- `src/app`: routing, shell and reactive application state.
- `src/features`: dashboard, vocabulary, languages (Japanese/Chinese), reading, listening, speaking, writing, settings, account, achievements, game (60-second race), assistant (AI tutor: `Chat.tsx` shared chat, `ChatWidget.tsx` corner mini chat in the app shell, full page).
- `src/services`: storage, SRS, speech, alignment, CSV, writing feedback and `auth` (API session), `sync` (account merge) and `community` (profile, badges, leaderboard) `game`, `recommend` (dashboard daily plan) and `assistant`.
- `src/data`: original JSON learning content and startup Zod validation.
- `src/components`, `src/i18n`: shared accessible controls and bilingual strings.
- `src/test`: test setup and integration coverage; `docs`: content authoring guide; `scripts`: content generators.
- `server/EnglishUp.Api`: Web API (`/api/*`), ASP.NET Identity endpoints, sync, points (`Points.cs`) profile/badge/leaderboard (`Community.cs`) quiz game (`Game.cs`) content search (`Knowledge.cs`: chunks, Gemini embeddings, pgvector) and the RAG assistant (`Assistant.cs`, shared Gemini client in `Gemini.cs`, evaluation in `Evaluation.cs`) endpoints, all reading `src/data` JSON linked into the build, EF Core migrations in `Data/Migrations`.
- `server/EnglishUp.Api.Tests`: xUnit API tests on an in-memory database.

## Commands

Client: `npm install`, `npm run dev`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run preview`, `npm run format`.

Server (from `server/`): `dotnet run --project EnglishUp.Api` (port 5080; needs `ConnectionStrings:Default` in user-secrets, migrates in Development), `dotnet run --project EnglishUp.Api -- ingest` (embeds `src/data` content; needs `Gemini:ApiKey`), `dotnet run --project EnglishUp.Api -- eval ../docs/eval/assistant-questions.json <report.md>` (30 questions, uses the Gemini quota), `dotnet test` (fake embedder and answerer, never Gemini), `dotnet tool restore` then `dotnet ef migrations add <Name> --project EnglishUp.Api -o Data/Migrations`.

## Conventions

Use typed services for business rules, keep user data in Dexie, use the shared attempt log for every skill. Never persist audio. Secrets (AI keys, database connection strings) live only on the server via user-secrets or environment variables, never in the Vite bundle or the repository. Auth tokens stay out of Dexie and JSON backups. The browser reaches the API only through same-origin `/api` (Vite proxy), never Supabase directly. UI labels must support vi/en; English learning content remains English. Validate imports and synced data before a transaction. A new synced store needs a version field in `sync.ts` and an entry in the server's store list. Use semantic controls and visible keyboard focus. Original content only.

## Definition of done

All four client checks and `dotnet test` pass after each milestone; conventional commit per milestone. Each skill completes and records a persisted attempt; backups survive reset/import. Add meaningful service and flow tests. Document limitations and assumptions. Do not claim microphone hardware was verified without real evidence.
