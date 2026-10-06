# Japanese and Chinese starter spaces

The sidebar learning-language picker is separate from the Vietnamese/English UI language. English retains its existing courses. Japanese and Mandarin Chinese (simplified script) each have a distinct home screen and three original beginner lessons across vocabulary, reading, listening, speaking and writing. This is a starter collection, not a complete JLPT/HSK curriculum.

Content lives in `src/data/languages.json`, validated at module load with Zod. Each lesson needs a unique prefixed ID, target script, romaji/pinyin, bilingual meaning, original short passage, bilingual question/options and a valid answer index. Add original content only.

Attempts use the shared Dexie log with an explicit learningLanguage. Historical attempts without that field belong to English. Settings without a target language default to English on load/import. Backup version 1 remains compatible; it includes the new settings/attempt fields and writing submissions. No database index migration is needed because filtering is currently in memory.

Listening uses installed browser speech voices with ja-JP or zh-CN; availability and pronunciation depend on the device. Speaking explicitly records self-assessed completion, not measured pronunciation accuracy; no microphone or audio recording is used. Hardware was not verified. Writing compares a short phrase to one model after width/space/punctuation normalization and stores submitted text; alternative correct translations are not recognized. Unsubmitted answers are session-only and switching languages discards them. Learning progress is isolated; display settings and backup/reset apply to the whole app.
