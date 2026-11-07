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

## Thesis roadmap — "EnglishUp với trợ giảng AI dựa trên RAG" (due 2027-01-04)

Accounts, server-side points, achievements and leaderboard, a 60-second quiz game, personalised recommendations and a RAG teaching assistant, on React → ASP.NET Core Web API → SQL Server.

1. Week 1 (Nov 9–15): API skeleton, ASP.NET Identity, sign-in/registration UI. **Done.**
2. Week 2: SQL tables mirroring the seven Dexie stores, push/pull sync, import a local backup into an account.
3. Week 3: server-side points with a daily cap, achievement rules, weekly/all-time leaderboard.
4. Week 4: 60-second multiple-choice game with combos and records; recommendations from weak skills/topics and due cards.
5. Weeks 5–6: RAG knowledge base from bundled content, retrieval with cited sources, server-side LLM proxy, chat UI, evaluation set.
6. Week 7: hardening, demo data, Docker run, screenshots. Week 8: report.

- Week 1 completed: `server/` solution with ASP.NET Core 9 minimal API, EF Core SQL Server (LocalDB by default), ASP.NET Identity API endpoints under `/api` (register, login, refresh, manage/info) with bearer tokens, 8-character complex passwords, unique emails and lockout. Vite proxies `/api`. The client adds an `auth` service (token refresh, offline-tolerant session restore) and an **Account** page linked from the top-bar avatar. Client: lint, typecheck, 107 tests in 23 files and build pass. Server: 9 xUnit tests pass. Browser check against LocalDB: weak password rejected, registration, reload persistence, sign-out and sign-in. Learning data is not synced yet.

## Translation extension

Added bidirectional word/sentence writing inside Vocabulary, 16 original bilingual sentences, reference matching with explicit equivalent-answer self-assessment, and persisted vocabulary attempts independent of SRS. All four checks passed (34 tests). Browser verification completed and saved a sentence in both directions.
