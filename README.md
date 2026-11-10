# EnglishUp

A local-first English practice space for Vietnamese-speaking learners. React 18 + strict TypeScript + Vite, React Router, Tailwind CSS, Zustand, Dexie and Zod. App branding is centralized in `src/app/App.tsx` (`APP_NAME`) and `index.html`.

## Run

Use Node.js 22.12+ (tested with Node 24) and npm.

```sh
npm install
npm run dev
```

Open the localhost URL printed by Vite. `npm run build` creates `dist`; `npm run preview` serves it locally. Keep the same origin/port to retain access to the same IndexedDB data. A deployed SPA needs a fallback to `index.html`.

### Optional account server

Accounts need the ASP.NET Core API (.NET 9 SDK) and a PostgreSQL database hosted on [Supabase](https://supabase.com). The browser never talks to Supabase: only the API holds the connection string.

1. Create a Supabase project (a region near your learners, e.g. Singapore) and note the database password.
2. In the dashboard choose **Connect → Session pooler** and copy the host and user (`postgres.<project-ref>`). The session pooler works over IPv4; the direct connection needs IPv6.
3. Store the connection string in user-secrets (kept outside the repository), then run the API:

```sh
cd server
dotnet user-secrets set "ConnectionStrings:Default" "Host=<pooler-host>;Port=5432;Database=postgres;Username=postgres.<project-ref>;Password=<database-password>;SSL Mode=Require" --project EnglishUp.Api
dotnet run --project EnglishUp.Api
```

It listens on `http://localhost:5080`, applies EF Core migrations to that database in Development, and Vite proxies `/api` to it. In production set the `ConnectionStrings__Default` environment variable instead. Free Supabase projects pause after a week without traffic; resume the project in the dashboard before a demo. Signed-in learners sync automatically when the app opens and on **Account → Sync now**. Without the server, everything except **Account** keeps working. Run `dotnet test` in `server/` for API tests.

The **AI tutor** page needs a [Gemini API key](https://aistudio.google.com) in user-secrets and the learning content embedded once into the database. Re-run `ingest` after changing many lessons at once; it only embeds new or changed items (admin edits are embedded as they are saved). The free tier embeds 100 items a minute and 1,000 a day (resetting at midnight Pacific time, about 15:00 in Vietnam), so the first ingest of about 2,100 items needs three runs on three days; lessons are embedded before vocabulary, and the command stops with a message when the daily quota runs out.

```sh
dotnet user-secrets set "Gemini:ApiKey" "<your-key>" --project EnglishUp.Api
dotnet run --project EnglishUp.Api -- ingest
```

**Learning content lives in the database.** Every English lesson (2,864 items: 2,475 words, 100 sentence patterns, 13 tenses, readings, listening, dictation, speaking, writing, translation sentences, synonym/antonym entries, 133 fill-in-the-blank grammar questions and 5 learning paths) is a row of `ContentItems` in Supabase. The app downloads it from `GET /api/content` before the first page renders and keeps a copy in IndexedDB (Dexie table `lessons`), so practice works offline after the first visit; with no network and no copy it shows a "lessons could not be loaded" notice. The server answers a repeat download with `304 Not Modified` (ETag). The JSON files in `src/data` are seed data only: in Development the API fills an empty `ContentItems` table from them at startup, and `dotnet run --project EnglishUp.Api -- seed` adds any seed item the database lacks (`seed --overwrite` puts the seed's version back on items an admin edited). Tests load the same files. Japanese and Chinese practice (postponed) still reads its bundled JSON.

**Admin dashboard** (`/admin`): make an existing account an admin, then sign out and in again. Signing in with an admin account opens the admin page, a separate page with its own header (no learning sidebar). Learner accounts open the learning app and are sent back to it from `/admin`. Admins can still open the learning app from the header, and its sidebar then shows an _Admin_ item. It shows how many accounts are online (the app was open in the last two minutes; signed-in clients send a heartbeat every minute) or offline, today's activity, and every account ordered by when it was last seen. Admins can search, lock or unlock accounts and hide a learner from the leaderboard. A locked learner's current access token still works until it expires (at most an hour); the refresh token stops at once. The _Learning content_ area adds, edits, hides and deletes (after a confirmation) every kind of English lesson: vocabulary, sentence patterns, readings, listening lessons, dictations, speaking and writing prompts, translation sentences and synonym/antonym entries. Every kind has its own form with labelled fields: lists take one entry per line, and dialogue lines and questions are repeatable blocks that can be added or removed. A new item starts blank, with the minimum number of questions. Before saving, the form lists empty fields and the app's schema issues, and Save stays disabled until there are none. Changes reach learners the next time they open the app. Words feed the 60-second race at once. Each save, hide or delete also re-embeds that one item for the AI tutor (one embedding call; dictation, speaking, translation and synonym items are not part of the tutor's knowledge). If Gemini is unavailable or the daily quota is used up, the change is still saved and the next `ingest` embeds it.

```sh
dotnet run --project EnglishUp.Api -- admin <email>
dotnet run --project EnglishUp.Api -- admin <email> --remove
```

For a presentation, `demo` adds six demo learners whose names end in "(demo)" with two weeks of practice, points and badges, so the leaderboard is not empty. They have no password, so nobody can sign in as them. Running it again replaces them; `demo remove` deletes them and everything they own.

```sh
dotnet run --project EnglishUp.Api -- demo
dotnet run --project EnglishUp.Api -- demo remove
```

## Checks

```sh
npm run lint
npm run typecheck
npm test
npm run build
```

## Assumptions

- Single learner per browser profile. Accounts (email + password, ASP.NET Identity bearer tokens) are optional. Signing in merges the progress already in this browser into the account, so do not sign a different learner into a browser that holds someone else's progress.
- Signed-in learners earn points on the server for each attempt synced for the first time: 1 + floor(score / 25), so 1–5, capped at 300 points per day (Vietnam time). Attempts older than seven days, for example from an imported backup, are kept without points.
- Six badges (first practice, 3- and 7-day streaks, all five skills, ten perfect scores, 100 reviewed words) add one-off bonus points outside the daily cap. Streaks use attempt timestamps from the device. The **Achievements** leaderboard lists only learners who opted in on **Account**, by display name, never by email; weeks start on Monday, Vietnam time.
- The **games** page (`/game`) has two 60-second races. Both need an account and the server, which draws the questions, keeps the answers and grades each one, so they cannot be played offline. The _vocabulary race_ asks for a word's Vietnamese meaning. The _grammar race_ shows a sentence with one blank and four options, from 133 original questions on 15 grammar points: tenses, articles, prepositions, adverbs, comparison, conditionals and wishes, the passive, modals, verb forms, linking words, relative clauses, quantifiers, pronouns, reported speech and inversion. Each question is tagged A1–C2 and can be filtered by level and grammar point. A wrong grammar answer shows why the right one is right. Score = 10 × correct + 5 × best combo; a game adds score / 10 points within the daily cap. Each race has its own record and a leaderboard (`GET /api/game/leaderboard?mode=&period=week|all`) of every shown learner's best game this week (from Monday, Vietnam time) or ever. Games are not recorded as skill attempts.
- The **level test** (`/placement`) has 30 questions, 5 per level from A1 to C2 (3 grammar blanks and 2 word meanings each), drawn from the library and easiest first. Score = right answers / 30 × 100. The estimated level is the highest level with at least 3 of 5 right on it and on every level below, so lucky guesses higher up do not count. The result is saved as a practice attempt and in the learner's settings (synced with an account), and it links to the matching learning path.
- **Learning paths** (`/roadmap`): A1→A2, A2→B1, B1→B2, B2→C1 and C1→C2, each with 4 stages and 12 tasks. A task opens the right practice page at its level, or a race at its level and grammar point. Learners tick tasks off, and progress per path is kept in their settings. Readings, listening, speaking, writing and translations exist at A2–B2 only, so the B2→C1 and C1→C2 paths use the hardest B2 lessons for those skills and say so. Admins edit both the questions and the paths on the admin page.
- The **AI tutor** opens from a button in the bottom-right corner of every page (Enter sends, Shift+Enter adds a line, Escape closes; the chat stays open across pages) and has a full page with the conversation list. It is signed-in only and answers from the five closest lesson chunks with Gemini `gemini-3.6-flash` at minimal thinking, cites them as [n] with links to the skill page, and keeps conversations on the server; deleting one erases its text, but its questions still count toward the daily limit. Each learner may ask 20 questions a day; answers can be wrong, and questions go to Google's free tier, so the page warns learners not to enter personal information. `dotnet run --project EnglishUp.Api -- eval ../docs/eval/assistant-questions.json <report.md>` scores it on 30 fixed questions (retrieval hit@1/hit@5/MRR, cited the expected source, no citations for 2 uncovered questions).
- Content search for the assistant (`GET /api/knowledge/search`, signed-in only) embeds the question with Gemini `gemini-embedding-2` (768 dimensions) and ranks the app's own words, readings, listening scripts, writing tasks, sentence patterns and tenses by cosine similarity in pgvector. On the free tier Google may use what is sent to improve its products, so only learning content and the question are sent. Each search uses one of the free tier's embeddings (100 a minute, 1,000 a day, shared by the whole server and by ingest); when they run out the API answers 503.
- The **daily plan** on the dashboard is computed in the browser from local attempts and due review cards: due cards first, then untried skills, then the lowest recent average plus 5 points per day since last practice. It is a rule-based heuristic, not a proficiency estimate, and speaking scores may be self-assessed.
- Sync merges both ways when the app opens, shortly after each new attempt and on demand: attempts are append-only by ID; settings, custom words, reviews, drafts, submissions and word-group progress keep the newest version (`updated`, `lastReviewed` or `timestamp`; last write wins, so clocks matter). Deletions and **Reset** affect only the device: a deleted custom word or reset data returns on the next sync. Each sync transfers the whole account, which suits one learner's history but not very large ones.
- The access token lasts one hour and is refreshed automatically with a 14-day refresh token. Tokens are kept in `localStorage`, outside Dexie and backups. Signing out deletes them on this device; the server does not revoke issued tokens. Email confirmation and password reset emails are not configured.
- Daily goal is elapsed practice minutes between starting and saving an attempt, rounded down on the dashboard. Idle time in an open exercise counts; close the session when finished. Dates use the learner's local timezone.
- English vocabulary spans A1–C2. CEFR labels guide study and do not certify a word's exam level or predict an IELTS band.
- English vocabulary can be studied without a daily card cap. The daily minute goal only tracks practice time.
- English, Japanese and Chinese are available as learning languages. UI can switch between Vietnamese and English; Vietnamese meanings and learner-error explanations are intentional pedagogical content.
- Writing feedback is an offline heuristic, not a proficiency certification. Optional LLM and stretch goals are deferred until the complete MVP is stable.
- Dependency major versions are not constrained except React 18. Router and Vitest use patched releases selected during installation.

## Privacy and limitations

All settings, reviews, attempts, custom vocabulary, drafts and submissions live in IndexedDB. Browser storage can be cleared or evicted: export backups regularly. Restoring a backup replaces existing data after validation inside a transaction. Audio blobs exist only in memory and are released when leaving the speaking session.

Microphone recording requires HTTPS or localhost and explicit browser permission. SpeechRecognition support varies, is mainly available in Chrome/Edge, and may send audio to a browser vendor service that needs internet. Read the speaking notice before enabling transcription. Without recognition, use recording and self-assessment. TTS voices depend on the OS/browser; some voices need connectivity. No audio or transcription is sent by EnglishUp to an application server.

EnglishUp is an installable PWA (`vite-plugin-pwa`). The production build precaches the app, fonts, icons and bundled lessons (about 2.5 MB) on the first visit, so after that the app opens and practice works with no network; install it from the browser's Install / Add to Home screen option. Account sync, points, the 60-second race, the leaderboard, the AI tutor and browser speech recognition still need a connection; an "Offline" sign shows when it is missing, and practice saved meanwhile syncs when the connection returns. The service worker never caches `/api`. It runs only in production builds (`npm run build` then `npm run preview`), not in `npm run dev`. IndexedDB is required; blocked storage displays an error rather than pretending to save.

## What is included

| Area                 | Features                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vocabulary           | 2,475 English entries across 65 topics, including 150 IELTS Writing collocations (15 themed topics in their own section, B1–C1), 200 phrasal verbs (exam topic, A1–C1), 220 IT terms for programming, web, databases, networking, security, testing, device support and cloud operations. Also includes Marketing, Economics, Finance, Law, Healthcare, Hospitality and C1–C2 academic practice. Four practice modes, selectable 20-word groups, skip/resume, SM-2 reviews, topic search, 30-card library pages, custom words and CSV. Existing IPA remains; new IPA awaits review.                                                |
| Reading              | 6 original passages, 30 questions including True/False/Not Given and short answers, exact evidence, reading timer/WPM, word lookup and manual dictionary additions                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Listening            | 6 original dialogues/talks, 24 questions, 12 dictation sentences, sentence replay, speaker voices/pitch, speed multipliers and gated transcripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Speaking             | 8 read-aloud/shadowing targets and 8 topic prompts, in-memory recording/replay, opt-in recognition, word alignment, 60–120 second timer, WPM/filler/variety metrics and self-assessment                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Writing              | 10 prompts across email/opinion/description/story, autosaved drafts, offline FeedbackProvider, structure checklist, submission history and draft comparison                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Grammar (`/grammar`) | Two parts. **Tenses** (`?part=tenses`): the 12 tenses plus be going to, on a past/present/future timeline; each has its affirmative, negative and question forms, uses with spoken examples, signal words, a tip on a common mistake and a three-question quick check saved as a `grammar` attempt. **Sentence patterns**: 100 English patterns in 12 groups (linking, too/enough, verb + to-V/V-ing, comparisons, perfect tenses, cause and effect…), each with formula, Vietnamese meaning, an original example with the pattern highlighted, translation and speech; 10-question gap-fill practice saved as a `grammar` attempt |
| Dashboard & settings | Vietnamese/English UI, shared level/topic filters, daily plan, streak, goal, skill averages, activity history, theme/accent/rate controls and full JSON backup/reset/restore                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

## Usage

Start with the dashboard or choose a skill in the navigation. Filters carry between modules during the current app session. In vocabulary, choose Everyday, Work & study, Specialist or Advanced exam; search or select a topic, then choose a group of up to 20 words and a practice mode. Reveal/check and rate recall, or skip without revealing. An incorrect typed/choice response requires Again. Ratings and skips save the position immediately; reopening the same level/topic resumes at the next unfinished card. Completed groups can be replayed explicitly.

For reading and listening, answer every question and select Check answer. Explanations and evidence appear after submission. Listening transcripts stay hidden until submission unless the setting explicitly permits them. Tap/click any transcript or passage word to consult the local dictionary; unknown words can be entered manually.

For speaking, listen to the model, then record. Recognition is off by default because browser services may process audio remotely. Review the recording/transcript and complete the self-assessment confirmation to save. A text match score is not acoustic pronunciation analysis. Manual notes are never misrepresented as an automatically recognized transcript.

Writing saves after each edit to IndexedDB. Submit to store a snapshot and feedback; edit and submit again to compare versions. Scores are deterministic heuristic checks. The provider cannot judge whether an argument is true or whether every task requirement is satisfied, so the checklist remains important.

Under Settings, Export backup saves a versioned JSON snapshot of all seven stores, including word-group progress. Restore validates the entire file, requests replacement confirmation, then replaces data atomically. Reset requires typing `RESET`. Use JSON for complete restoration; vocabulary CSV only transfers card content. Keep backups outside the browser.

## Scoring and scheduling assumptions

- SM-2 qualities: Again 1, Hard 3, Good 4, Easy 5. Successful intervals begin at 1 and 6 days, then multiply by the previous ease factor. Ease has a 1.3 floor. Again resets repetitions and schedules tomorrow. Group access is not limited by the review schedule.
- A card is New before its first review, Learning below a 21-day interval, and Mastered at 21 days or more. This is an app label, not proof of permanent retention.
- Dashboard attempt count includes individual vocabulary ratings and one result per submitted skill exercise. Practice averages combine objective, heuristic and explicitly self-assessed scores; they are not directly comparable proficiency measures.
- Word accuracy is `max(0, 1 − word edit distance / target word count) × 100`. Contractions, case and punctuation are normalized. Common ambiguous contractions are expanded conventionally (e.g. “he's” → “he is”); context-sensitive parsing is outside the MVP. Alignment is bounded to the first 1,000 normalized words.
- Reading WPM uses the explicit Finished reading time, or the full exercise time if that button is not used. Speaking WPM requires a recording duration. Vocabulary variety is unique normalized words divided by total words; filler counting is a simple pattern heuristic and can count meaningful uses of “like”.
- A streak counts local calendar dates with any saved attempt; an unpracticed current day does not break yesterday's streak until the following day.

## Architecture and extension

See [DESIGN.md](DESIGN.md) for the visual system, [AGENTS.md](AGENTS.md) for structure/conventions and [docs/CONTENT.md](docs/CONTENT.md) for all JSON schemas, accepted answers and CSV examples. [docs/TESTING.md](docs/TESTING.md) describes automated coverage and real-device checks. `src/services/feedback.ts` exports the `FeedbackProvider` interface for a future optional provider. No LLM endpoint, API key or proxy is included in this MVP.

The app uses semantic form controls, explicit labels, keyboard focus, a skip link, textual diff labels alongside colors, responsive layouts and light/dark palettes. It uses system fonts and CSS illustrations without external asset requests. Feature routes load lazily. No stack deviation was necessary.

Recommended follow-ups after MVP acceptance: test physical microphones and OS voices on your target devices, have an English teacher and subject specialists review CEFR labels, IPA and content, then consider an offline service worker and optional LLM feedback. Real-device voice quality and a formal WCAG audit remain outside automated verification.

## Translation practice

Vocabulary → Translation practice supports words and sentences in both Vietnamese → English and English → Vietnamese directions. It uses bundled/custom words and 16 original bilingual sentences across eight topics. Filters apply to the next session of up to ten randomly selected items, independently of due-card limits. Check, compare references, then save each result. Saved vocabulary attempts are included in backups and dashboard averages without changing SRS; leaving the tab discards only the unsaved exercise.

Matching ignores case, punctuation and whitespace while preserving Vietnamese accents. It is not semantic grading: equivalent alternatives require explicit self-assessment and are labelled in history. Matches/self-assessed equivalents score 100; other answers score 0.
