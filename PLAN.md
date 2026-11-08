# EnglishUp implementation plan

## Assumptions

- Build a local-first single-user MVP in this empty repository using the requested stack.
- Original bundled learning content covers A2–B2; A1/C1 filters show an honest empty state.
- Speech availability depends on the browser; recording and self-assessment remain available independently of recognition.
- Offline rule-based writing feedback is the MVP; the optional LLM provider and stretch features are out of scope.

## Milestones

1. Scaffold React 18, strict TypeScript, Vite, Tailwind, routing, bilingual shell, Dexie and settings.
2. Vocabulary content, custom decks/CSV, four practice modes and SM-2 scheduling.
3. Reading passages, questions, evidence and dictionary/save flow.
4. Listening scripts, sentence playback, exercises and shared word alignment.
5. Speaking recording, recognition, read-aloud and topic-talk assessment.
6. Writing drafts, rule-based feedback, history and comparisons.
7. Dashboard, unified attempts, progress and validated data backup/restore.
8. Accessibility and error-state polish, smoke tests, content documentation and README.

## Verification

After every milestone run lint, typecheck, tests and production build, fix failures, then create a conventional commit when Git is available. Final checks include persistent attempts and export/reset/import round trip. Verify browser UI when a browser automation surface is available. Microphone/audio require a real device and permission; report any unverified hardware behavior honestly.

- Milestone 1 completed: lint, typecheck, storage round-trip test and production build passed. Dependencies audited: zero findings.
- Milestone 2 completed: 160 validated words, four practice modes, SM-2, custom words and CSV. All four checks passed (6 tests).
- Milestone 3 completed: six original reading passages, 30 questions, evidence, reading timer/WPM, dictionary and custom-word save. All four checks passed (7 tests).
- Milestone 4 completed: six listening scripts, 24 questions, 12 dictations, sentence replay, transcript gates and word alignment. All four checks passed (10 tests).
- Milestone 5 completed: 8 read-aloud and 8 topic prompts, opt-in recognition, in-memory recording, timers, metrics and explicit self-assessment fallback. All four checks passed (11 tests); real microphone hardware remains unverified.
- Milestone 6 completed: 10 writing prompts, autosaved drafts, rule-based FeedbackProvider, persistent history and draft comparisons. All four checks passed (14 tests).
- Milestone 7 completed: dashboard with daily plan, streaks, goal minutes, due cards, per-skill averages, week chart and persisted activity. Backup/reset/restore tested across all six stores. All four checks passed (17 tests).
- Milestone 8 completed: bilingual accessibility/error-state polish, lazy route loading, recorder cleanup and permission tests, five-skill integration flows, content authoring guide and full README. All four checks passed (26 tests). Browser checks covered every skill, reload persistence, narrow and dark layouts, and downloaded-backup/reset/restore. Physical audio hardware remains unverified; see docs/TESTING.md.

## Thesis roadmap — "EnglishUp với trợ giảng AI dựa trên RAG" (code and report done by 2027-01-03, submission 2027-01-04)

Accounts, server-side points, achievements and leaderboard, a 60-second quiz game, personalised recommendations and a RAG teaching assistant, on React → ASP.NET Core Web API → PostgreSQL (Supabase).

Done before the plan was reset on 2026-11-08: accounts (ASP.NET Identity), account sync, move to Supabase Postgres.

1. Week 1 (Nov 9–15): server-side points ledger with a daily cap, sync right after each attempt. Report: chapter 1.
2. Week 2 (Nov 16–22): learner profiles (display name, leaderboard opt-in, time zone), achievements, weekly/all-time leaderboard. Report: chapter 2 part 1.
3. Week 3 (Nov 23–29): 60-second multiple-choice game, server-generated and server-graded, combos and records. Report: chapter 3 part 1.
4. Week 4 (Nov 30–Dec 6): recommendations from weak skills and due cards; choose the LLM and embedding providers; mid-term review. Report: chapter 3 part 2.
5. Week 5 (Dec 7–13): RAG ingestion (pgvector, chunks, embeddings) and retrieval API. Report: chapter 2 part 2.
6. Week 6 (Dec 14–20): assistant API with citations, chat UI, history, rate limits, 30-question evaluation set. Report: chapter 4 part 1.
7. Week 7 (Dec 21–27): hardening, demo data, deployment or local demo, screenshots. Report: chapter 4 part 2.
8. Week 8 (Dec 28–Jan 3): code freeze Dec 30, report, slides, rehearsal, tag v1.0.

Cut order if late: game records, number of badges, recommendations beyond the weakest skill, online deployment. Never cut the cited RAG assistant and its evaluation.

- Accounts completed (old week 1): `server/` solution with ASP.NET Core 9 minimal API, EF Core SQL Server (LocalDB by default), ASP.NET Identity API endpoints under `/api` (register, login, refresh, manage/info) with bearer tokens, 8-character complex passwords, unique emails and lockout. Vite proxies `/api`. The client adds an `auth` service (token refresh, offline-tolerant session restore) and an **Account** page linked from the top-bar avatar. Client: lint, typecheck, 107 tests in 23 files and build pass. Server: 9 xUnit tests pass. Browser check against LocalDB: weak password rejected, registration, reload persistence, sign-out and sign-in. Learning data is not synced yet.
- Sync completed (old week 2): SQL Server `Attempts` (typed, for points/leaderboards) and `SyncRecords` (settings, words, reviews, drafts, submissions, vocabularyStudy as versioned JSON) with cascade delete per user; authenticated `POST /api/sync` validates the payload, merges (attempts append-only, newest version wins) and returns the account. The client syncs on startup, after sign-in and from **Account**, validates the response with Zod before one Dexie transaction, and reloads settings. Importing a local backup then syncing moves it into the account. Client: lint, typecheck, 110 tests in 24 files and build pass. Server: 19 xUnit tests pass. Browser check against LocalDB: a vocabulary rating and theme reached SQL Server, survived a local reset via sync with no duplicates, and an offline sync showed the error while keeping the session. Deletions are not synced (no tombstones).
- Database moved from SQL Server to PostgreSQL on Supabase (Npgsql 9.0.4, single `InitialCreate` migration, connection string in user-secrets) for pgvector and a hosted database; the API, Identity and sync logic are unchanged. Server: 19 xUnit tests pass. Checked against the Supabase project (Singapore, session pooler, Data API disabled): migration applied, register/login, 401 without a token, sync merge (append-only attempts, newest review kept) and 400 on an invalid payload.
- Week 1 completed: `PointLedger` (unique per learner/source/source id) and `GET /api/points`. Sync awards 1 + floor(score / 25) points (1–5) for attempts first saved, capped at 300 points per Vietnam calendar day; attempts older than seven days are kept without points. The client syncs 1.5 s after any new attempt while signed in and shows today/total points on **Account**; settings reload after every sync. Vite ignores `server/` because Visual Studio locks `server/.vs`. Client: lint, typecheck, 113 tests and build pass. Server: 29 xUnit tests pass. Checked on Supabase: `AddPoints` applied, one Easy flashcard gave 5 points, a reload re-synced without double counting. Learner profiles and per-learner time zones move to week 2.
- Week 2 completed: `LearnerProfiles` (generated display name, hidden until the learner opts in) and `UserAchievements` (migration `AddCommunity`); six badge rules in `Community.cs` (first practice, 3- and 7-day streaks, all five skills, ten perfect scores, 100 reviewed words) awarded after each sync with bonus points outside the daily cap; `GET/PUT /api/profile`, `GET /api/achievements`, `GET /api/leaderboard?period=week|all` (top 50, Monday-based Vietnam week, opted-in learners only). New **Achievements** page (badges, leaderboard tabs, hidden-learner notice) and a profile form on **Account**. Per-learner time zones were dropped: all learners use Vietnam time. Client: lint, typecheck, 118 tests and build pass. Server: 46 xUnit tests pass. Checked on Supabase: `AddCommunity` applied, first-practice badge awarded on sync, profile saved, the learner appeared first on the weekly and all-time leaderboards. Design: [docs/DATABASE.md](docs/DATABASE.md).

## Translation extension

Added bidirectional word/sentence writing inside Vocabulary, 16 original bilingual sentences, reference matching with explicit equivalent-answer self-assessment, and persisted vocabulary attempts independent of SRS. All four checks passed (34 tests). Browser verification completed and saved a sentence in both directions.
