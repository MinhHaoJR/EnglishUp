# EnglishUp

A local-first English practice space for Vietnamese-speaking learners. React 18 + strict TypeScript + Vite, React Router, Tailwind CSS, Zustand, Dexie and Zod. App branding is centralized in `src/app/App.tsx` (`APP_NAME`) and `index.html`.

## Run

Use Node.js 22.12+ (tested with Node 24) and npm.

```sh
npm install
npm run dev
```

Open the localhost URL printed by Vite. `npm run build` creates `dist`; `npm run preview` serves it locally. Keep the same origin/port to retain access to the same IndexedDB data. A deployed SPA needs a fallback to `index.html`.

## Checks

```sh
npm run lint
npm run typecheck
npm test
npm run build
```

## Assumptions

- Single learner per browser profile, no account/backend or cross-device sync.
- Daily goal is elapsed practice minutes between starting and saving an attempt, rounded down on the dashboard. Idle time in an open exercise counts; close the session when finished. Dates use the learner's local timezone.
- Original content covers A2–B2; A1 and C1 are supported filters with an empty state until content is added.
- New cards per day is a global limit; overdue reviews do not consume it.
- English is the learning language. UI can switch between Vietnamese and English; Vietnamese word meanings and learner-error explanations are intentional pedagogical content.
- Writing feedback is an offline heuristic, not a proficiency certification. Optional LLM and stretch goals are deferred until the complete MVP is stable.
- Dependency major versions are not constrained except React 18. Router and Vitest use patched releases selected during installation.

## Privacy and limitations

All settings, reviews, attempts, custom vocabulary, drafts and submissions live in IndexedDB. Browser storage can be cleared or evicted: export backups regularly. Restoring a backup replaces existing data after validation inside a transaction. Audio blobs exist only in memory and are released when leaving the speaking session.

Microphone recording requires HTTPS or localhost and explicit browser permission. SpeechRecognition support varies, is mainly available in Chrome/Edge, and may send audio to a browser vendor service that needs internet. Read the speaking notice before enabling transcription. Without recognition, use recording and self-assessment. TTS voices depend on the OS/browser; some voices need connectivity. No audio or transcription is sent by EnglishUp to an application server.

Static assets must load before local practice can run. This MVP is not an installable PWA and does not guarantee cold-start offline navigation. Keep the app open for network-free rule-based exercises. IndexedDB is required; blocked storage displays an error rather than pretending to save.

## What is included

| Area                 | Features                                                                                                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vocabulary           | 160 words across 8 topics, General American IPA, Vietnamese meanings, definitions and examples; four practice modes; SM-2 review queue; search, topic decks, custom word editing and CSV |
| Reading              | 6 original passages, 30 questions including True/False/Not Given and short answers, exact evidence, reading timer/WPM, word lookup and manual dictionary additions                       |
| Listening            | 6 original dialogues/talks, 24 questions, 12 dictation sentences, sentence replay, speaker voices/pitch, speed multipliers and gated transcripts                                         |
| Speaking             | 8 read-aloud/shadowing targets and 8 topic prompts, in-memory recording/replay, opt-in recognition, word alignment, 60–120 second timer, WPM/filler/variety metrics and self-assessment  |
| Writing              | 10 prompts across email/opinion/description/story, autosaved drafts, offline FeedbackProvider, structure checklist, submission history and draft comparison                              |
| Dashboard & settings | Vietnamese/English UI, shared level/topic filters, daily plan, streak, goal, skill averages, activity history, theme/accent/rate controls and full JSON backup/reset/restore             |

## Usage

Start with the dashboard or choose a skill in the navigation. Filters carry between modules during the current app session. In vocabulary, select a mode and review up to ten due/new cards. Reveal or check the answer, then rate recall. An incorrect typed/choice response requires Again. Each rated card saves immediately; leaving early retains completed reviews.

For reading and listening, answer every question and select Check answer. Explanations and evidence appear after submission. Listening transcripts stay hidden until submission unless the setting explicitly permits them. Tap/click any transcript or passage word to consult the local dictionary; unknown words can be entered manually.

For speaking, listen to the model, then record. Recognition is off by default because browser services may process audio remotely. Review the recording/transcript and complete the self-assessment confirmation to save. A text match score is not acoustic pronunciation analysis. Manual notes are never misrepresented as an automatically recognized transcript.

Writing saves after each edit to IndexedDB. Submit to store a snapshot and feedback; edit and submit again to compare versions. Scores are deterministic heuristic checks. The provider cannot judge whether an argument is true or whether every task requirement is satisfied, so the checklist remains important.

Under Settings, Export backup saves a versioned JSON snapshot of all six stores. Restore validates the entire file, requests replacement confirmation, then replaces data atomically. Reset requires typing `RESET`. Use JSON for complete restoration; vocabulary CSV only transfers card content. Keep backups outside the browser.

## Scoring and scheduling assumptions

- SM-2 qualities: Again 1, Hard 3, Good 4, Easy 5. Successful intervals begin at 1 and 6 days, then multiply by the previous ease factor. Ease has a 1.3 floor. Again resets repetitions and schedules tomorrow. A learner may raise the new-card limit in Settings.
- A card is New before its first review, Learning below a 21-day interval, and Mastered at 21 days or more. This is an app label, not proof of permanent retention.
- Dashboard attempt count includes individual vocabulary ratings and one result per submitted skill exercise. Practice averages combine objective, heuristic and explicitly self-assessed scores; they are not directly comparable proficiency measures.
- Word accuracy is `max(0, 1 − word edit distance / target word count) × 100`. Contractions, case and punctuation are normalized. Common ambiguous contractions are expanded conventionally (e.g. “he's” → “he is”); context-sensitive parsing is outside the MVP. Alignment is bounded to the first 1,000 normalized words.
- Reading WPM uses the explicit Finished reading time, or the full exercise time if that button is not used. Speaking WPM requires a recording duration. Vocabulary variety is unique normalized words divided by total words; filler counting is a simple pattern heuristic and can count meaningful uses of “like”.
- A streak counts local calendar dates with any saved attempt; an unpracticed current day does not break yesterday's streak until the following day.

## Architecture and extension

See [AGENTS.md](AGENTS.md) for structure/conventions and [docs/CONTENT.md](docs/CONTENT.md) for all JSON schemas, accepted answers and CSV examples. [docs/TESTING.md](docs/TESTING.md) describes automated coverage and real-device checks. `src/services/feedback.ts` exports the `FeedbackProvider` interface for a future optional provider. No LLM endpoint, API key or proxy is included in this MVP.

The app uses semantic form controls, explicit labels, keyboard focus, a skip link, textual diff labels alongside colors, responsive layouts and light/dark palettes. It uses system fonts and CSS illustrations without external asset requests. Feature routes load lazily. No stack deviation was necessary.

Recommended follow-ups after MVP acceptance: test physical microphones and OS voices on your target devices, have an English teacher review CEFR/IPA/content, then consider an offline service worker, more A1/C1 content and optional LLM feedback. Real-device voice quality and a formal WCAG audit remain outside automated verification.

## Translation practice

Vocabulary → Translation practice supports words and sentences in both Vietnamese → English and English → Vietnamese directions. It uses bundled/custom words and 16 original bilingual sentences across eight topics. Filters apply to the next session of up to ten randomly selected items, independently of due-card limits. Check, compare references, then save each result. Saved vocabulary attempts are included in backups and dashboard averages without changing SRS; leaving the tab discards only the unsaved exercise.

Matching ignores case, punctuation and whitespace while preserving Vietnamese accents. It is not semantic grading: equivalent alternatives require explicit self-assessment and are labelled in history. Matches/self-assessed equivalents score 100; other answers score 0.
