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
