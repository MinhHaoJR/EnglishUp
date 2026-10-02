# EnglishUp

Local-first Vietnamese/English learning app. React 18, strict TypeScript, Vite, Tailwind, Zustand, Dexie. No server and no secret keys.

## Structure

- `src/app`: routing, shell and reactive application state.
- `src/features`: dashboard, vocabulary, reading, listening, speaking, writing, settings.
- `src/services`: storage, SRS, speech, alignment, CSV and writing feedback.
- `src/data`: original JSON learning content and startup Zod validation.
- `src/components`, `src/i18n`: shared accessible controls and bilingual strings.
- `src/test`: test setup and integration coverage; `docs`: content authoring guide.

## Commands

`npm install`, `npm run dev`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run preview`, `npm run format`.

## Conventions

Use typed services for business rules, keep user data in Dexie, use the shared attempt log for every skill. Never persist audio or API secrets. UI labels must support vi/en; English learning content remains English. Validate imports before a transaction. Use semantic controls and visible keyboard focus. Original content only.

## Definition of done

All four quality checks pass after each milestone; conventional commit per milestone. Each skill completes and records a persisted attempt; backups survive reset/import. Add meaningful service and flow tests. Document limitations and assumptions. Do not claim microphone hardware was verified without real evidence.
