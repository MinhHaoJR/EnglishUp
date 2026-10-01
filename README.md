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
- Daily goal is minutes of active practice. Dates use the learner's local timezone.
- Original content covers A2–B2; A1 and C1 are supported filters with an empty state until content is added.
- New cards per day is a global limit; overdue reviews do not consume it.
- English is the learning language. UI can switch between Vietnamese and English; Vietnamese word meanings and learner-error explanations are intentional pedagogical content.
- Writing feedback is an offline heuristic, not a proficiency certification. Optional LLM and stretch goals are deferred until the complete MVP is stable.
- Dependency major versions are not constrained except React 18. Router and Vitest use patched releases selected during installation.

## Privacy and limitations

All settings, reviews, attempts, custom vocabulary, drafts and submissions live in IndexedDB. Browser storage can be cleared or evicted: export backups regularly. Restoring a backup replaces existing data after validation inside a transaction. Audio blobs exist only in memory and are released when leaving the speaking session.

Microphone recording requires HTTPS or localhost and explicit browser permission. SpeechRecognition support varies, is mainly available in Chrome/Edge, and may send audio to a browser vendor service that needs internet. Read the speaking notice before enabling transcription. Without recognition, use recording and self-assessment. TTS voices depend on the OS/browser; some voices need connectivity. No audio or transcription is sent by EnglishUp to an application server.

Static assets must load before local practice can run. This MVP is not an installable PWA and does not guarantee cold-start offline navigation. Keep the app open for network-free rule-based exercises. IndexedDB is required; blocked storage displays an error rather than pretending to save.
