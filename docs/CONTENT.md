# Adding original learning content

All six UTF-8 JSON files in `src/data/` are parsed with Zod when the application module loads. TypeScript types are inferred from `schema.ts`; validation is not a type assertion. `npm test` verifies quantities, passage lengths, unique IDs, accepted choices and evidence. Invalid content must be fixed before shipping.

Use original writing. Do not paste textbook, examination, news or copyrighted exercise material. The supplied content was authored for EnglishUp; CEFR labels are editorial estimates, not exam certification. Vietnamese meanings and General American IPA are teaching aids and can be refined by an educator.

## Shared fields

Every item has a stable unique `id`, a `level` (`A1`, `A2`, `B1`, `B2`, `C1`) and a `topic`. The original topics are `Daily life`, `Travel`, `Work`, `Food`, `Health`, `Technology`, `Environment`, `Education`; the vocabulary expansion adds the eight topics listed below. Update `topics` and `topicVi` in `src/i18n/index.ts` when adding another topic. Keep IDs stable so saved reviews and drafts retain their meaning.

## Vocabulary — vocabulary.json

The catalog now contains 240 words across 16 topics. In addition to the original eight topics, `Shopping` and `Communication` contain 10 words each. Six specialist groups contain 10 words each: `IT: Programming`, `IT: Web development`, `IT: Databases`, `IT: Networking`, `IT: Security`, and `IT: Testing and deployment`. These original examples describe common technical concepts; specialist terms carry estimated B1–B2 reading levels, not certified CEFR ratings.

The vocabulary page separates everyday topics from IT, displays counts for the selected level, and groups library results by topic. Topic selection applies to practice, translation practice, and CSV export through the existing shared filters. Search accepts Vietnamese with or without accents and filters the visible library only. Imported/custom topics are included automatically. New topics add vocabulary exercises; they do not add reading, listening, or sentence-translation lessons, so those filters can return no lessons. Existing bundled IDs and stored reviews remain unchanged; the 80 additions use stable `v-extra-` IDs. All words remain bundled for offline use.

```json
{
  "id": "my-word-001",
  "word": "lantern",
  "ipa": "/ˈlæntɚn/",
  "pos": "noun",
  "meaning": "đèn lồng",
  "definition": "a light inside a protective case",
  "examples": ["A paper lantern hung above the table."],
  "level": "B1",
  "topic": "Daily life"
}
```

`examples` must contain one or two nonempty strings. Keep General American IPA between slashes. `custom: true` is used for user-created/imported entries, not bundled entries. The original 160 words were authored in `scripts/create-vocabulary.mjs`; it is retained as provenance. Edit the JSON directly for new content; rerunning that script overwrites the JSON with its original authored set.

## Questions

```json
{
  "id": "my-reading-q1",
  "type": "choice",
  "prompt": "Where did they meet?",
  "options": ["At the park", "At the station", "At home"],
  "answers": ["At the park"],
  "explanation": "The first paragraph identifies the meeting place.",
  "evidence": "They met at the park."
}
```

- `choice`: two or more options; every accepted answer must be present in `options`.
- `tfng`: omit `options`; the UI supplies `True`, `False`, `Not Given`. Use exactly one of these strings in `answers`.
- `short` and `blank`: omit options and list accepted variants, e.g. `["15", "fifteen", "15 minutes"]`.
- Matching ignores case, extra spaces and terminal punctuation. It does not infer synonyms, so include reasonable variants explicitly.
- `evidence` must occur verbatim in the passage/script. For Not Given, cite the related statement and explain exactly what information is absent.

## Reading — reading.json

Fields: `id`, `title`, `level`, `topic`, `text`, `questions`. Separate paragraphs in `text` with `\n\n`. Each passage has 150–350 whitespace-separated words and exactly five questions, mixing choice, tfng and short answer. There are six original passages (30 questions). The dictionary tokenizes words and matches bundled/custom entries case-insensitively; it does not perform stemming. Missing terms open a manual entry form.

## Listening — listening.json and dictation.json

Listening fields: `id`, `title`, `level`, `topic`, `lines`, `questions`. Each line is `{ "speaker": "Mai", "text": "Are you free on Saturday?" }`. Speaker names determine the voice index; when only one suitable voice exists, pitch alternates. Use one sentence per line when precise sentence replay is desired. The UI additionally splits longer turns into sentences for playback. Each lesson requires four or five questions, usually a mix of `choice` and `blank`.

Dictation fields: `id`, `text`, `level`, `topic`. There are 12 original sentences. The target remains hidden until submission, unless the learner has explicitly enabled always-show-transcript.

## Speaking — speaking.json

Fields: `id`, `title`, `level`, `topic`, `mode`, `text`, `cues`. `mode` is `read` (target text for alignment) or `talk` (topic prompt). `cues` is a nonempty array of speaking tips or guiding questions. Supply at least eight prompts per mode. Topic sessions can be set to 60, 90 or 120 seconds; shorter practice can be saved with a reminder.

## Writing — writing.json

Fields: `id`, `title`, `level`, `topic`, `genre`, `prompt`, `minWords`, `maxWords`, `checklist`. Genre is `email`, `opinion`, `description` or `story`. The maximum word target must be at least the minimum; the checklist needs at least three items. Targets guide feedback and are not editor hard limits. There are ten original prompts covering all four genres.

## CSV vocabulary interchange

Required UTF-8 header names (order can vary):

```csv
word,ipa,pos,meaning,definition,examples,level,topic
lantern,/ˈlæntɚn/,noun,đèn lồng,a light inside a protective case,A lantern lit the room.,B1,Daily life
```

Quote cells containing commas/newlines; double embedded quotes. Two examples are separated by `||`. Every row is validated before writing. Import adds new custom cards with fresh IDs; it does not overwrite existing words and can create duplicates if imported repeatedly. CSV exports honor level/topic filters; the search box only filters the visible library. Export prefixes formula-like values with an apostrophe for spreadsheet safety. JSON backup is the lossless full-data format and includes SRS state, unlike CSV.

## Backup v1

Top-level fields: `version: 1`, `settings`, `words`, `reviews`, `attempts`, `drafts`, `submissions`. Full runtime schemas live in `src/services/storage.ts`. All timestamps are Unix milliseconds; attempt duration is seconds. `settings.id` is always `main`. Reviews store ease, interval in days, repetitions, due date, introduction date, last review and accuracy counters. IDs in each table must be unique. Import validates all tables before a single atomic replacement transaction. Recordings and transient filters are never included.

## Bilingual translation sentences

`src/data/translations.json` contains original paired sentences. Each record has a unique `id`, a supported `level`, `topic`, and nonempty `en` / `vi` arrays of accepted translations. The first entry is the prompt for the opposite direction; subsequent entries are accepted alternatives. Startup validates the schema and duplicate IDs. Add natural equivalents instead of relying on automatic semantic grading. Word exercises derive English terms and Vietnamese meanings from the existing vocabulary, including custom words; commas and semicolons separate accepted individual meanings.
