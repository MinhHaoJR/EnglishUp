# Adding original learning content

This guide covers English learning content. See [Japanese and Chinese learning spaces](languages.md) for the separate 2,000-entry catalogs, source format and vocabulary practice.

The UTF-8 English lesson JSON files in `src/data/` are parsed with Zod when their application modules load. TypeScript types are inferred from `schema.ts`; validation is not a type assertion. `npm test` verifies quantities, passage lengths, unique IDs, accepted choices and evidence. Invalid content must be fixed before shipping.

Use original writing. Do not paste textbook, examination, news or copyrighted exercise material. The supplied content was authored for EnglishUp; CEFR labels are editorial estimates, not exam certification. Vietnamese meanings and General American IPA are teaching aids and can be refined by an educator.

## Shared fields

Every standard lesson has a stable unique `id`, a `level` (`A1`, `A2`, `B1`, `B2`, `C1`, `C2`) and a `topic`. The topic registry and Vietnamese display names live in `topics` and `topicVi` in `src/i18n/index.ts`; update both when adding a topic. Keep IDs stable so saved reviews and drafts retain their meaning. C2 vocabulary is available in the advanced exam topics and the separate word-relations collection below; other skill/level selections may have no lessons. Custom words, CSV and backups also support C2.

## English synonyms and antonyms

Open **Vocabulary → Synonyms & antonyms**, or `/vocabulary?tab=relations`. The separate, original collection contains 72 headword lessons, 12 at each CEFR level A1–C2. Each teaches one selected sense with an English definition, Vietnamese meaning, original example, one near-synonym, one antonym, related-word meanings/examples and bilingual usage notes. These are 144 directed lexical relations, not synonyms automatically generated for every word in the general vocabulary catalog.

The [Council of Europe defines six CEFR proficiency levels](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions). [English Vocabulary Profile](https://englishprofile.org/?menu=english-vocabulary-profile) emphasizes individual meanings, not just whole words. The collection uses **editorial lesson difficulty**, guided by the selected sense and context. Related words may have different difficulty or register. Labels are not individually certified word ratings, an IELTS/TOEIC score conversion, or proof of exam readiness. Synonyms are often near-equivalents; an antonym applies to the sense stated on the card. All definitions, examples and usage explanations were written for this app, not copied from dictionary entries.

Source files: `src/data/wordRelations-basic.json` (A1–B1) and `src/data/wordRelations-advanced.json` (B2–C2). `src/data/wordRelations.ts` validates required fields, supported levels, unique headwords/IDs, matching level prefixes, and distinct headword/synonym/antonym strings. Preserve the selected part of speech and check real contextual opposition when editing. Structural validation cannot replace a professional linguistic review.

The collection has its own level, relation-type and accent-insensitive search controls, independent of general vocabulary topic filters. At most 12 cards render per library page. Practice selects up to 10 distinct entries from the current level/search selection. Each two-option question contrasts the authored synonym and antonym for the selected sense, so random unrelated words do not introduce extra plausible answers. Mixed practice alternates the requested relation type. Successful saves use the shared English vocabulary attempt log; scores are 100 or 0, and labels include relation type, lesson level and headword. Existing SRS schedules are unaffected. Attempts survive the existing backup/reset/import flow without a database migration. Unsaved choices and in-progress session position are temporary.

## Vocabulary — vocabulary.json

The catalog contains **1,920 distinct entries across 47 topics**: 1,620 general entries, 60 IT terms, 160 new specialist terms and 80 academic/exam practice expressions. The original common expansion added 1,440 authored entries to the previous 240, including 901 A1 entries. Everyday topics cover family, home, food, clothes, the body, common verbs and adjectives, places, time, nature, animals, transport, hobbies, school, relationships, money, function words, numbers and colors. Counts include multiword expressions; the catalog is an editorial learning selection, not a corpus-ranked frequency list.

The first advanced expansion added 60 B2 and 60 C1 entries across `Work`, `Education`, `Environment`, `Technology`, `Communication`, and `Ideas and relationships`. The current level totals are A1: 901, A2: 479, B1: 94, B2: 226, C1: 180 and C2: 40. Every new entry has a Vietnamese meaning, original English definition and contextual example, and a part of speech. Existing records and review IDs are preserved. C1 and C2 work with the same filters, practice, CSV and backup flows; no reset is needed. CEFR labels are editorial estimates, not independently assessed classifications or a conversion to an IELTS band.

The newer specialist collection provides 20 entries each for `Marketing: Strategy`, `Marketing: Digital`, `Economics: Macroeconomics`, `Economics: Markets`, `Finance: Investing`, `Law: Contracts`, `Healthcare: Clinical work` and `Hospitality: Service`. Each has ten B2 and ten C1 entries. The advanced exam section offers 20 entries each for academic argument, evidence and research, society and policy, and language and nuance; each topic has ten C1 and ten C2 entries. This is practice for precise academic reading and writing, **not an official IELTS or CEFR vocabulary list**. IELTS assesses lexical range and appropriate use in context in its [writing guidance](https://ielts.org/take-a-test/preparation-resources/writing-test-resources); the [Council of Europe describes C1/C2 as broad, nuanced proficiency](https://www.coe.int/en/web/common-european-framework-reference-languages/table-%201-cefr-3.3-common-reference-levels-global-scale). Definitions and examples were written for EnglishUp. Specialist meanings may vary by profession and jurisdiction; an educator or domain professional should review them before formal use.

Six specialist groups retain 10 terms each: `IT: Programming`, `IT: Web development`, `IT: Databases`, `IT: Networking`, `IT: Security`, and `IT: Testing and deployment`. CEFR labels are approximate teaching levels. Each general entry includes a Vietnamese meaning, part of speech, short English definition and original contextual example. Only a selected sense is taught for words with multiple meanings. New IPA fields are intentionally empty pending pronunciation review; existing IPA is preserved and browser speech remains available where supported.

The vocabulary page groups topics under **Everyday**, **Work & study**, **Specialist**, **Advanced exam**, plus **Custom** when needed. The topic picker and its dropdown are grouped; topic-name search works with or without Vietnamese accents. Counts reflect the selected level, and topics with zero matching words are disabled. The library renders at most 30 word cards per page, with previous/next buttons and a page selector. Search or level/topic changes return to page one; disappearing custom words cannot leave the library on a nonexistent page. Topic selection applies to practice, translation practice and CSV export through the existing shared filters. Library search filters the visible words, while CSV exports the entire level/topic selection. New topics add vocabulary exercises; they do not add reading, listening or sentence-translation lessons, so those filters can return no lessons. All previous 1,680 records and IDs remain unchanged. New entries use stable `v-extended-<term>` IDs. Content remains bundled for offline use; no database migration or reset is required.

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

The common and specialist expansions are authored in `scripts/content/common-vocabulary.txt` and `scripts/content/extended-english-vocabulary.txt`: a header `@Topic|part of speech|level` followed by `word|Vietnamese meaning|English definition|example` rows. Run `node scripts/expand-vocabulary.mjs` after editing either source to regenerate the `v-common-` and `v-extended-` entries in `vocabulary.json`. The generator preserves the original 240 records, rejects duplicate words/IDs and malformed rows, and writes only after validation. Repeated runs are deterministic. Edit these sources rather than their generated JSON records. Keep headwords stable to preserve review IDs and saved study positions.

The original 160 words were authored in `scripts/create-vocabulary.mjs`, retained as historical provenance only. Do not run that older script to update the current catalog: it overwrites the expanded JSON with its original set. Content tests check quantity, topic labels, unique headwords and contextual examples; flow tests cover pagination, A1 practice, CSV and backup/restore of new-card progress.

## English vocabulary practice groups

The main vocabulary practice screen divides the current level/topic selection into fixed groups of 20 words in catalog order; the last group can be shorter. Choose a group, preview its words and start any of the four practice modes. There is no daily new-word cap. The daily minute goal is informational; the legacy `settings.newCards` field is retained only for compatibility with existing backups and no longer limits practice.

Each level/topic combination has its own selected group and visited word IDs in Dexie. Rating or skipping a card saves its position immediately. Ending early leaves the unanswered current card available for the next visit; previously rated/skipped cards are excluded until the learner explicitly chooses **Review this group** after completing it. Switching practice mode shares the same position. Existing SRS reviews seed the visited IDs on first use of a selection, avoiding an immediate repeat of previously studied words. Later visits use the saved traversal; the SRS schedule remains a suggestion and does not block group access. Skipping creates neither a score nor an SRS review. Rating saves the review, shared attempt and traversal atomically.

Progress survives reload and JSON backup/reset/import. Level/topic filters themselves remain temporary, so choose the same filters to resume that selection. Group membership follows the current catalog, including custom words; editing or removing words can change group boundaries. IDs retain visited history, and a removed group anchor falls back to an unfinished group. Japanese/Chinese practice and the separate translation/word-relations modes keep their existing session behavior.

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

Top-level fields: `version: 1`, `settings`, `words`, `reviews`, `attempts`, `drafts`, `submissions`, `vocabularyStudy`. Full runtime schemas live in `src/services/storage.ts`. All timestamps are Unix milliseconds; attempt duration is seconds. `settings.id` is always `main`. Reviews store ease, interval in days, repetitions, due date, introduction date, last review and accuracy counters. `vocabularyStudy` stores the selected group and unique visited word IDs per English level/topic selection. Older backups without this field import with an empty progress table. Dexie schema version 2 adds this seventh table without replacing existing data; the JSON backup format remains version 1 with an additive optional field. IDs in each table must be unique. Import validates all tables before a single atomic replacement transaction. Recordings and transient filters are never included.

## Bilingual translation sentences

`src/data/translations.json` contains original paired sentences. Each record has a unique `id`, a supported `level`, `topic`, and nonempty `en` / `vi` arrays of accepted translations. The first entry is the prompt for the opposite direction; subsequent entries are accepted alternatives. Startup validates the schema and duplicate IDs. Add natural equivalents instead of relying on automatic semantic grading. Word exercises derive English terms and Vietnamese meanings from the existing vocabulary, including custom words; commas and semicolons separate accepted individual meanings.
