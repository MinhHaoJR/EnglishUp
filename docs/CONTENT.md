# Adding original learning content

All six UTF-8 JSON files in `src/data/` are parsed with Zod when the application module loads. TypeScript types are inferred from `schema.ts`; validation is not a type assertion. `npm test` verifies quantities, passage lengths, unique IDs, accepted choices and evidence. Invalid content must be fixed before shipping.

Use original writing. Do not paste textbook, examination, news or copyrighted exercise material. The supplied content was authored for EnglishUp; CEFR labels are editorial estimates, not exam certification. Vietnamese meanings and General American IPA are teaching aids and can be refined by an educator.

## Shared fields

Every item has a stable unique `id`, a `level` (`A1`, `A2`, `B1`, `B2`, `C1`) and a `topic`. The topic registry and Vietnamese display names live in `topics` and `topicVi` in `src/i18n/index.ts`; update both when adding a topic. Keep IDs stable so saved reviews and drafts retain their meaning.

## Vocabulary — vocabulary.json

The catalog contains **1,560 distinct entries across 35 topics: 1,500 general vocabulary entries and 60 IT terms**. The expansion adds 1,320 original entries to the previous 240, including 901 A1 entries. New topics cover family, home, food, clothes, the body, common verbs and adjectives, places, time, nature, animals, transport, hobbies, school, relationships, money, function words, numbers and colors. Counts include useful multiword expressions and calendar names; this is an editorial selection for everyday learning, not a corpus-ranked top-1,500 frequency list.

Six specialist groups retain 10 terms each: `IT: Programming`, `IT: Web development`, `IT: Databases`, `IT: Networking`, `IT: Security`, and `IT: Testing and deployment`. CEFR labels are approximate teaching levels. Each general entry includes a Vietnamese meaning, part of speech, short English definition and original contextual example. Only a selected sense is taught for words with multiple meanings. New IPA fields are intentionally empty pending pronunciation review; existing IPA is preserved and browser speech remains available where supported.

The vocabulary page separates everyday topics from IT, displays counts for the selected level, and groups library results by topic. The library renders at most 30 word cards per page, with previous/next buttons and a page selector. Search or level/topic changes return to page one; disappearing custom words cannot leave the library on a nonexistent page. Topic selection applies to practice, translation practice, and CSV export through the existing shared filters. Search accepts Vietnamese with or without accents and filters the visible library only. CSV exports the entire level/topic selection, not just the visible page. Imported/custom topics are included automatically. New topics add vocabulary exercises; they do not add reading, listening, or sentence-translation lessons, so those filters can return no lessons. All previous 240 records and IDs remain unchanged. New entries use stable `v-common-<term>` IDs. Content remains bundled for offline use; no database migration or reset is required.

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

`examples` must contain one or two nonempty strings. Verified General American IPA belongs between slashes; leave `ipa` empty when no reviewed transcription is available. `custom: true` is used for user-created/imported entries, not bundled entries.

The common expansion is authored in `scripts/content/common-vocabulary.txt`: a header `@Topic|part of speech|level` followed by `word|Vietnamese meaning|English definition|example` rows. Run `node scripts/expand-vocabulary.mjs` after editing it to regenerate the `v-common-` entries in `vocabulary.json`. The generator preserves every other record, rejects duplicate words/IDs and malformed rows, and writes only after validation. Repeated runs are deterministic. Edit this source rather than its generated JSON records. Keep headwords stable to preserve review IDs.

The original 160 words were authored in `scripts/create-vocabulary.mjs`, retained as historical provenance only. Do not run that older script to update the current catalog: it overwrites the expanded JSON with its original set. Content tests check quantity, topic labels, unique headwords and contextual examples; flow tests cover pagination, A1 practice, CSV and backup/restore of new-card progress.

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
