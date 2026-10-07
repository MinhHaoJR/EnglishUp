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
