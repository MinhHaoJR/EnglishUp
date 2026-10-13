# Verification and manual device checks

Run `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` after changing content or code. The Vitest suite uses jsdom and fake IndexedDB; it exercises actual React components and storage services rather than replacing the core flows with mocks.

Automated coverage includes SM-2 progression/failure/ease floor/new-card budget, local-calendar streaks, word alignment and dictation scoring, writing rules, CSV quoting/Unicode/rejection, startup content validation, all five module flows, draft restoration, dashboard reconstruction, atomic backup/reset/import, microphone-denial fallback and recording resource cleanup. Audio-device tests mock browser media APIs; they do not prove microphone hardware or vendor recognition works.

For a real-device check:

1. Open the app on localhost or HTTPS in Chrome/Edge. Start a speaking prompt, leave recognition off, grant microphone access, record and stop. Play your recording. Navigate away and verify the microphone indicator stops.
2. Enable browser recognition only if you accept its vendor processing. Record again, check the transcript, then test with internet unavailable. Recording/self-assessment should remain usable even when recognition fails.
3. Try both English accents and the three listening speed multipliers. Installed OS voices determine available accents and sound quality.
4. Use only Tab, Shift+Tab, Enter, Space and arrow keys for navigation, questions, rating buttons, settings, file selection and dictionary lookup. Verify focus indicators and the skip link.
5. Test a narrow phone viewport and both themes. Content should wrap without page-level horizontal scrolling; the navigation intentionally scrolls horizontally on narrow screens.
6. Complete a session in every skill, reload, and check recent activity. Export JSON, reset via the typed confirmation, import the file and compare the restored history, words, reviews, settings, drafts and submissions.

Use a separate test profile for manual resets. The app never uploads backups or persists audio. Do not treat a rule score or self-assessed speaking score as a standardized language assessment.

## Recorded verification — 2026-10-02

- Automated suite: 26 tests across 10 files; lint, strict typecheck and production build passed.
- Browser: completed vocabulary (10 cards), reading, listening, speaking self-assessment and writing. Reload preserved all 14 attempts and the dashboard's five skill summaries.
- Downloaded the JSON backup, performed the typed reset, selected the downloaded file and confirmed restore. All 14 attempts and dashboard scores returned, together with the saved English/dark preferences. The downloaded file contained 10 reviews, one draft and one submission; automated round-trip coverage additionally verifies custom words and all six stores.
- Inspected desktop light/dark layouts and a 390 × 844 viewport. No page-level horizontal overflow was observed; mobile navigation scrolls intentionally. Browser console checks showed no warnings or errors during the tested flows.
- Returned the preview to Vietnamese/light settings. The preview profile contains synthetic practice activity from these checks.
- Physical microphone capture, audible TTS quality and vendor speech recognition remain unverified. Follow the device checklist above before relying on them.

## Translation extension verification

The suite now contains 34 passing tests in 12 files. New coverage includes Unicode normalization with Vietnamese accents preserved, alternative word meanings, bounded random sessions, both directions for words and sentences, filter selection, empty-answer prevention, incorrect score persistence, unchanged SRS and explicit self-assessed labels. Browser checks also completed the Health/A2 sentence in both directions and verified saved-session feedback. See translation-preview.jpg for the reference-answer screen.

## Continue learning

Reading, listening, dictation, speaking and writing show Continue after the current
attempt is saved successfully. It opens the next lesson in the current level/topic
filter (and speaking mode); the final lesson returns to the lesson list. Session
answers, feedback and timers reset on the next lesson. Writing drafts remain stored
per prompt. Editing a submitted writing draft requires saving the updated work
before continuing. Unfinished exercises must be completed or left with Back.
Microphone hardware was not verified for this navigation change.

## Japanese/Chinese vocabulary and interface — 2026-10-10

- Both source catalogs contain exactly 2,000 unique entries across 20 topics. Startup schemas and content tests cover IDs, language prefixes, required fields, script/readings and topic registration. Rebuilding twice produces identical output.
- All 74 tests across 17 files pass, including accent-free search, topic deep links, bounded pagination, same-language answer options, overlapping-gloss exclusion, double-click prevention, failed-save retry, continuation, session completion and persistence across remount/backup/reset/import. Existing English skill flows remain covered.
- Lint, strict TypeScript and production build pass. The lazily loaded multilingual catalog chunk is about 701 kB (138 kB gzip); Vite reports its default 500 kB size advisory. English does not load this chunk until the user opens a Japanese/Chinese workspace.
- Browser checks in an isolated Edge context covered desktop and 375 px mobile layouts, Japanese dark cards/quiz, Chinese dark home, pinyin search without tone marks, saving an answer and continuing with a fresh question. No page-level horizontal overflow or browser page errors were observed. Preview: `languages-preview.jpg`.
- First 600 entries per language received a separate editorial spot review; additional topic entries received structural checks and sampled reading/meaning review. This is not a full professional lexicographic review. Browser speech availability and audible pronunciation quality remain device-dependent; microphone hardware was not tested.

## Colorful learning studio — 2026-10-11

- Refreshed the shared navigation, English dashboard and learning pages, and Japanese/Chinese home, library and quiz surfaces. A violet shell anchors orange listening, rose speaking, blue reading and teal writing cues. Topic labels accompany every topic color. Shared SVG navigation icons and CSS illustrations work without external image or font requests.
- Retained existing routes, settings, learning content, persisted attempts and Dexie schema. Dashboard lesson counts now come directly from the content arrays. Vietnamese/English UI labels remain supported.
- Lint, strict TypeScript, all 74 tests in 17 files and the production build pass. The existing approximately 701 kB multilingual catalog chunk advisory remains; this milestone does not change content loading.
- Isolated Edge browser checks covered home and all five skill routes in all three learning languages, both themes, and 375, 768 and 1440 px viewports. No page-level horizontal overflow or page errors were observed. The mobile navigation deliberately scrolls within its own row.
- Verified Japanese answer saving and continuation, Chinese pinyin search without tone marks, English UI on a narrow viewport, visible keyboard focus on the primary learning link and reduced-motion styling. Tablet hero artwork is hidden to give the learning action enough space. Preview: `vibrant-preview.jpg`.
- These checks exercise browser rendering and existing storage flows, not physical touchscreen or audio hardware. No new service behavior or database migration is included.

## English word relations and CEFR levels — 2026-10-13

- Added 72 original, sense-specific headword lessons (12 each at A1, A2, B1, B2, C1 and C2), each with one near-synonym and one contextual antonym, examples and bilingual usage notes. The UI identifies the levels as editorial learning guidance; this is not an independently certified CEFR word list. Reviewed all relation pairs and notes; adjusted accept/take to a job-offer example so the taught replacement fits the context.
- All 84 tests across 19 files, lint, strict TypeScript and production build pass. New coverage checks invalid/overlapping relation data, level-specific search, bounded two-option sessions, correct/incorrect scores, duplicate-click prevention, failed-save retry, explicit continuation, full session completion, direct-link integration, and results surviving remount and backup/reset/import. C2 custom vocabulary also round-trips through CSV and JSON backup. Existing English/Japanese/Chinese flows remain covered.
- Browser checks in an isolated Edge profile verified all six level buttons show their 12 entries, light/dark layouts at 375/768/1440 px without page-level overflow, filtered one-question completion, a ten-question session's continuation reset, and visible keyboard focus. A saved C2 antonym result appeared on the English dashboard after reload. No browser page errors were observed. Preview: `word-relations-preview.jpg`.
- Existing settings and data are retained; there is no Dexie schema migration. General vocabulary topic filters do not restrict this new collection. Unsaved answers and session position are temporary; each saved answer is retained independently. The pre-existing approximately 701 kB multilingual catalog build advisory remains. Audio hardware was not tested for this feature.

## English vocabulary groups and resume — 2026-10-13

- Main vocabulary practice now offers fixed groups of up to 20 words, word previews, unrestricted daily study, a skip action before revealing answers, and saved traversal shared by flashcards, multiple choice, typing and spelling. Rating creates an attempt and SRS review; skipping only advances the saved position. Returning with the same level/topic filters resumes the selected group. Replaying a completed group is explicit.
- All 95 tests across 21 files pass, along with lint, strict TypeScript and the production build. Added coverage verifies group boundaries including a short last group, 45 rated words in one day, resumption after early exit and backup/reset/import, compatibility with old backups, additive Dexie v1-to-v2 migration, duplicate-click prevention, transactional rollback and retry, mode switching, zero legacy daily limits, and completion after skipping all 20 cards. The longer round-trip UI test has a 10-second timeout to accommodate the full parallel suite.
- An isolated Edge profile verified choosing group 2, skipping without revealing, rating, ending early, reloading and returning to exactly the third card (3/20). It also completed the group, immediately started another group, and checked that typing a correct answer advances with an empty input. No page errors occurred. Chooser and flashcards were checked in both themes at 375, 768 and 1440 px with no page-level horizontal overflow. Keyboard focus was visible on the group selector. Preview: `vocabulary-groups-preview.jpg`.
- Dexie v2 adds a seventh table for traversal without resetting existing stores. Backups include this progress; old backups default it to empty. Group boundaries follow the current catalog and may move when custom entries change. The daily minute goal remains informational, and the old `newCards` setting is ignored. The pre-existing approximately 701 kB multilingual build advisory remains. This milestone changes English main vocabulary practice; audio hardware was not tested.
