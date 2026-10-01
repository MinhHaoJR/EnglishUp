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
