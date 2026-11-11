# Adding original learning content

This guide covers English learning content. See [Japanese and Chinese learning spaces](languages.md) for the separate 2,000-entry catalogs, source format and vocabulary practice.

The English lessons live in the `ContentItems` table on the server; the UTF-8 JSON files in `src/data/` are their seed. After editing a seed file, run `dotnet run --project EnglishUp.Api -- seed` from `server/` to add new items, or `seed --overwrite` to also replace items already in the database (this discards admin edits to those items). Admins can instead edit single items on the admin page. The app validates every row with the Zod schemas in `schema.ts` (and `wordRelations.ts`) when it loads the library and skips invalid rows; TypeScript types are inferred from the same schemas. `npm test` loads the seed files and verifies quantities, passage lengths, unique IDs, accepted choices and evidence. Invalid seed content must be fixed before shipping.

Use original writing. Do not paste textbook, examination, news or copyrighted exercise material. The supplied content was authored for EnglishUp; CEFR labels are editorial estimates, not exam certification. Vietnamese meanings and General American IPA are teaching aids and can be refined by an educator.

## Shared fields

Every standard lesson has a stable unique `id`, a `level` (`A1`, `A2`, `B1`, `B2`, `C1`, `C2`) and a `topic`. The topic registry and Vietnamese display names live in `topics` and `topicVi` in `src/i18n/index.ts`; update both when adding a topic. Keep IDs stable so saved reviews and drafts retain their meaning. C2 vocabulary is available in the advanced exam topics and the separate word-relations collection below; other skill/level selections may have no lessons. Custom words, CSV and backups also support C2.

## English synonyms and antonyms

Open **Vocabulary → Synonyms & antonyms**, or `/vocabulary?tab=relations`. The separate, original collection contains 72 headword lessons, 12 at each CEFR level A1–C2. Each teaches one selected sense with an English definition, Vietnamese meaning, original example, one near-synonym, one antonym, related-word meanings/examples and bilingual usage notes. These are 144 directed lexical relations, not synonyms automatically generated for every word in the general vocabulary catalog.

The [Council of Europe defines six CEFR proficiency levels](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions). [English Vocabulary Profile](https://englishprofile.org/?menu=english-vocabulary-profile) emphasizes individual meanings, not just whole words. The collection uses **editorial lesson difficulty**, guided by the selected sense and context. Related words may have different difficulty or register. Labels are not individually certified word ratings, an IELTS/TOEIC score conversion, or proof of exam readiness. Synonyms are often near-equivalents; an antonym applies to the sense stated on the card. All definitions, examples and usage explanations were written for this app, not copied from dictionary entries.

Source files: `src/data/wordRelations-basic.json` (A1–B1) and `src/data/wordRelations-advanced.json` (B2–C2). `src/data/wordRelations.ts` validates required fields, supported levels, unique headwords/IDs, matching level prefixes, and distinct headword/synonym/antonym strings. Preserve the selected part of speech and check real contextual opposition when editing. Structural validation cannot replace a professional linguistic review.

The collection has its own level, relation-type and accent-insensitive search controls, independent of general vocabulary topic filters. At most 12 cards render per library page. Practice selects up to 10 distinct entries from the current level/search selection. Each two-option question contrasts the authored synonym and antonym for the selected sense, so random unrelated words do not introduce extra plausible answers. Mixed practice alternates the requested relation type. Successful saves use the shared English vocabulary attempt log; scores are 100 or 0, and labels include relation type, lesson level and headword. Existing SRS schedules are unaffected. Attempts survive the existing backup/reset/import flow without a database migration. Unsaved choices and in-progress session position are temporary.

## Vocabulary — vocabulary.json and vocabulary-it.json

The catalog contains **2,475 distinct entries across 65 topics**: 45 added common verbs, 150 IELTS Writing collocations and 200 phrasal verbs (see below) plus 1,620 general entries, 220 IT terms, 160 other specialist terms and 80 academic/exam practice expressions. The original common expansion added 1,440 authored entries to the previous 240, including 901 A1 entries. Everyday topics cover family, home, food, clothes, the body, common verbs and adjectives, places, time, nature, animals, transport, hobbies, school, relationships, money, function words, numbers and colors. Counts include multiword expressions; the catalog is an editorial learning selection, not a corpus-ranked frequency list.

The first advanced expansion added 60 B2 and 60 C1 entries across `Work`, `Education`, `Environment`, `Technology`, `Communication`, and `Ideas and relationships`. The current level totals are A1: 901, A2: 479, B1: 174, B2: 306, C1: 180 and C2: 40. Every new entry has a Vietnamese meaning, original English definition and contextual example, and a part of speech. Existing records and review IDs are preserved. C1 and C2 work with the same filters, practice, CSV and backup flows; no reset is needed. CEFR labels are editorial estimates, not independently assessed classifications or a conversion to an IELTS band.

The newer specialist collection provides 20 entries each for `Marketing: Strategy`, `Marketing: Digital`, `Economics: Macroeconomics`, `Economics: Markets`, `Finance: Investing`, `Law: Contracts`, `Healthcare: Clinical work` and `Hospitality: Service`. Each has ten B2 and ten C1 entries. The advanced exam section offers 20 entries each for academic argument, evidence and research, society and policy, and language and nuance; each topic has ten C1 and ten C2 entries. This is practice for precise academic reading and writing, **not an official IELTS or CEFR vocabulary list**. IELTS assesses lexical range and appropriate use in context in its [writing guidance](https://ielts.org/take-a-test/preparation-resources/writing-test-resources); the [Council of Europe describes C1/C2 as broad, nuanced proficiency](https://www.coe.int/en/web/common-european-framework-reference-languages/table-%201-cefr-3.3-common-reference-levels-global-scale). Definitions and examples were written for EnglishUp. Specialist meanings may vary by profession and jurisdiction; an educator or domain professional should review them before formal use.

The IT collection now has 220 terms. The original six topics—`IT: Programming`, `IT: Web development`, `IT: Databases`, `IT: Networking`, `IT: Security`, and `IT: Testing and deployment`—each contain 30 terms. `IT: Devices and support` and `IT: Cloud and operations` each contain 20. The 160 new entries are split evenly between editorial B1 and B2 levels and cover common workplace actions as well as technical concepts. Their English definitions and examples are original. Official [MDN web glossary](https://developer.mozilla.org/en-US/docs/Glossary), [Git glossary](https://git-scm.com/docs/gitglossary) and [NIST security glossary](https://csrc.nist.gov/glossary) served as terminology references; individual cards have not had a professional terminology review. These are a practical teaching selection, not a frequency-ranked or officially CEFR-rated list. Only a selected sense is taught for words with multiple meanings. New IPA fields are intentionally empty pending pronunciation review; existing IPA is preserved and browser speech remains available where supported.

The vocabulary page groups topics under **Everyday**, **Work & study**, **Specialist**, **Advanced exam**, plus **Custom** when needed. IT topics appear first in Specialist. The topic picker and its dropdown are grouped; topic-name search works with or without Vietnamese accents. Counts reflect the selected level, and topics with zero matching words are disabled. The library renders at most 30 word cards per page, with previous/next buttons and a page selector. Search or level/topic changes return to page one; disappearing custom words cannot leave the library on a nonexistent page. Topic selection applies to practice, translation practice and CSV export through the existing shared filters. Library search filters the visible words, while CSV exports the entire level/topic selection. New topics add vocabulary exercises; they do not add reading, listening or sentence-translation lessons, so those filters can return no lessons. All previous 1,920 records and IDs remain unchanged. New IT entries use stable `v-it-<term>` IDs. Content remains bundled for offline use; no database migration or reset is required.

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

The expansions are authored in `scripts/content/common-vocabulary.txt`, `scripts/content/extended-english-vocabulary.txt` and `scripts/content/it-vocabulary.txt`: a header `@Topic|part of speech|level` followed by `word|Vietnamese meaning|English definition|example` rows. Run `node scripts/expand-vocabulary.mjs` after editing a source to regenerate `v-common-` and `v-extended-` entries in `vocabulary.json`, plus `v-it-` entries in `vocabulary-it.json`. The `seed` command copies both files into the database in catalog order. The generator preserves the original 240 records, rejects duplicate words/IDs and malformed rows, and writes only after validation. Repeated runs are deterministic. Edit these sources rather than their generated JSON records. Keep headwords stable to preserve review IDs and saved study positions.

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

Fields: `id`, `title`, `level`, `topic`, `text`, `questions`. Separate paragraphs in `text` with `\n\n`. Each passage has 150–350 whitespace-separated words and exactly five questions, mixing choice, tfng and short answer. There are 300 passages (1,500 questions), 50 per level from A1 to C2. r1–r6 were written by hand; `python scripts/create-reading-passages.py` keeps them and writes r7–r300 from a compact format (a `## Title | topic` line, the paragraphs, then five `?` lines), refusing any passage outside 150–350 words, without exactly five questions or with evidence that is not an exact part of the text. Length and difficulty grow with the level: simple first-person texts at A1, everyday stories and messages at A2, articles at B1–B2, analytical essays at C1 and argumentative essays that test the writer's stance at C2. Titles are unique, because a saved attempt marks a passage done by its title. The dictionary tokenizes words and matches bundled/custom entries case-insensitively; it does not perform stemming. A word the dictionary lacks is added by an admin, not from the lesson.

## Listening — listening.json and dictation.json

Listening fields: `id`, `title`, `level`, `topic`, `lines`, `questions`. Each line is `{ "speaker": "Mai", "text": "Are you free on Saturday?" }`. Speaker names determine the voice index; when only one suitable voice exists, pitch alternates. Use one sentence per line when precise sentence replay is desired. The UI additionally splits longer turns into sentences for playback. Each lesson requires four or five questions, usually a mix of `choice` and `blank`. There are 300 lessons, 50 per level from A1 to C2. l1–l24 were written by hand; `python scripts/create-listening-lessons.py` keeps them and writes l25–l300 from a compact format (a `## Title | topic` line, `Speaker: text` lines, and one `?` line per question), refusing any lesson whose evidence is not an exact part of its script. Titles are unique, because a saved attempt marks a lesson done by its title. Length grows with the level, from about 45 words at A1 to 110–175 at C2; C1 lessons add discussion, register and idiom, and C2 lessons test implication, irony and hedged argument. `tfng` questions need no `options`. Every `evidence` is an exact substring of the script.

Dictation fields: `id`, `text`, `level`, `topic`. There are 12 original sentences. The target remains hidden until submission, unless the learner has explicitly enabled always-show-transcript.

## Speaking — speaking.json

Fields: `id`, `title`, `level`, `topic`, `mode`, `text`, `cues`. `mode` is `read` (target text for alignment) or `talk` (topic prompt). `cues` is a nonempty array of speaking tips or guiding questions. There are 300 prompts, 50 per level from A1 to C2, 25 of each mode. s1–s16 are the first hand-written set; `python scripts/create-speaking-prompts.py` keeps them and writes s17–s300 from one compact line per prompt. Read-aloud texts grow from one or two short sentences at A1 to a short paragraph at C2, and their cues are pronunciation tips (stress, pauses, linking). Topic talks give a task and three guiding points. Titles are unique, because a saved attempt marks a prompt done by its title. Topic sessions can be set to 60, 90 or 120 seconds; shorter practice can be saved with a reminder.

## Writing — writing.json

Fields: `id`, `title`, `level`, `topic`, `genre`, `prompt`, `minWords`, `maxWords`, `checklist`. Genre is `email`, `opinion`, `description` or `story`. The maximum word target must be at least the minimum; the checklist needs at least three items. Targets guide feedback and are not editor hard limits. There are 300 prompts, 50 per level from A1 to C2, covering all four genres. w1–w10 are the first hand-written set; `python scripts/create-writing-prompts.py` keeps them and writes w11–w300 from one compact line per prompt (title, topic code, genre code, prompt, checklist). Word targets grow with the level: A1 30–60, A2 60–100, B1 100–160, B2 160–250, C1 220–320, C2 280–400. Titles are unique, because a saved attempt marks a prompt done by its title.

## CSV vocabulary interchange

Required UTF-8 header names (order can vary):

```csv
word,ipa,pos,meaning,definition,examples,level,topic
lantern,/ˈlæntɚn/,noun,đèn lồng,a light inside a protective case,A lantern lit the room.,B1,Daily life
```

Quote cells containing commas/newlines; double embedded quotes. Two examples are separated by `||`. Every row is validated before writing. Import adds new custom cards with fresh IDs; it does not overwrite existing words and can create duplicates if imported repeatedly. CSV exports honor level/topic filters; the search box only filters the visible library. Export prefixes formula-like values with an apostrophe for spreadsheet safety. JSON backup is the lossless full-data format and includes SRS state, unlike CSV.

## Backup v1

Top-level fields: `version: 1`, `settings`, `words`, `reviews`, `attempts`, `drafts`, `submissions`, `vocabularyStudy`. Full runtime schemas live in `src/services/storage.ts`. All timestamps are Unix milliseconds; attempt duration is seconds. `settings.id` is always `main`. Reviews store ease, interval in days, repetitions, due date, introduction date, last review and accuracy counters. `vocabularyStudy` stores the selected group and unique visited word IDs per English level/topic selection. Older backups without this field import with an empty progress table. Dexie schema version 2 adds this seventh table without replacing existing data, and version 3 adds `lessons`, the offline copy of the server's lesson library, which backups, reset and import leave out; the JSON backup format remains version 1 with an additive optional field. IDs in each table must be unique. Import validates all tables before a single atomic replacement transaction. Recordings and transient filters are never included.

## Bilingual translation sentences

`src/data/translations.json` contains original paired sentences. Each record has a unique `id`, a supported `level`, `topic`, and nonempty `en` / `vi` arrays of accepted translations. The first entry is the prompt for the opposite direction; subsequent entries are accepted alternatives. The app validates each item's schema when it loads the library; tests check duplicate IDs. Add natural equivalents instead of relying on automatic semantic grading. Word exercises derive English terms and Vietnamese meanings from the existing vocabulary, including custom words; commas and semicolons separate accepted individual meanings.

## Grammar questions — grammar-quiz.json

Generated by `python scripts/create-grammar-quiz.py`; edit the item list there, rerun it, then run `seed` (or edit single questions on the admin page). Each item has an `id` (`q-<level>-NNN`), a `level`, a `category` (one of the 15 grammar points in `quizCategories`, `src/data/schema.ts`), a `sentence` with exactly one `___`, four different `options`, the `answer` (one of the options) and a Vietnamese `explanation` shown after a wrong answer. Write distractors that are clearly wrong in the sentence. Avoid a second option that is also grammatical, such as `will` beside `be going to` for a prediction from evidence. The grammar race draws from these items, and so does the level test (3 per level), so keep at least 3 per level. The seed has 133: A1 22, A2 25, B1 25, B2 25, C1 20, C2 16.

## Learning paths — roadmaps.json

Generated by `python scripts/create-roadmaps.py`. Each path has an id `rm-<from>-<to>` (consecutive levels), `weeks`, a bilingual `title` and `summary`, and `stages`. Each stage has a bilingual `title` and `goal` and `tasks`. A task has an `id` unique in the path, a `skill` (the page it opens: vocabulary, translation, relations, grammar, reading, listening, speaking, writing, wordgame, grammargame, assistant, placement), the `level` the page is filtered to, an optional `category` for a grammar race, and Vietnamese/English text. Learner progress is stored by task id, so renaming an id loses its tick.

## Phrasal verbs — vocabulary-phrasal.json

Generated by `python scripts/create-phrasal-verbs.py`. It holds 200 common phrasal verbs in the topic `Exam: Phrasal verbs` (Ôn thi: Cụm động từ, in the advanced exam section). Ids are `v-pv-<words>`, `pos` is `phrasal verb`, and IPA stays empty until reviewed. The headwords follow a common study list the project owner supplied. The Vietnamese meanings, English definitions, examples and levels (A1 8, A2 50, B1 83, B2 44, C1 15) were written for EnglishUp; no wording is copied from that list. Each example contains the headword in its base form, and entries are ordered by level, so the 20-word clusters go from easiest to hardest. After editing, run `seed`, then `ingest` for the tutor.

## IELTS Writing collocations — vocabulary-collocations.json

Generated by `python scripts/create-collocations.py`. It holds 150 collocations in 15 themed topics of ten (`Writing: Education` … `Writing: Economy and development`, shown as "Collocation: Giáo dục" and so on). They sit in their own topic section, `writing` ("Collocation IELTS Writing"). Ids are `v-col-<words>`, `pos` is `collocation`, and IPA stays empty. The headwords and themes follow a study list the project owner supplied. The Vietnamese meanings, English definitions, examples and levels (B1 1, B2 65, C1 84) were written for EnglishUp; no wording is copied from that list. Each example contains the headword exactly. After editing, run `seed`, then `ingest`.

## Added common verbs — vocabulary-verbs.json

Generated by `python scripts/create-common-verbs.py`. It holds 61 verbs from two study lists the project owner supplied that were not yet in the library. Of the first list's 141 distinct words, 96 already existed (mostly in Everyday verbs) and were skipped; of the second list's 30, 18 existed and 12 joined. A headword present as another word class (May, correct, mark, account) was skipped at first; its verb sense was then added as a separate entry on request, so those four headwords appear twice (once per word class). The script allows a repeat only for these four and only when no verb entry exists. The script refuses any headword already present. The verbs join the existing `Everyday verbs` topic (261 entries now), with ids `v-verb-<word>`. Their IPA comes from the supplied list (American transcriptions), unlike the other new entries, which wait for review. Meanings follow the verb sense; where the list gave a noun sense (set, point) or a loose gloss (regard, state), the meaning was corrected. Definitions and examples were written for EnglishUp.

## Tenses — tenses.json

Generated by `python scripts/create-tenses.py` and shown in Grammar → Tenses. It has 13 entries: the 12 tenses and be going to (present 4, past 4, future 5). Each has an id `t-<name>`, `order`, `group` (past, present, future), `level`, a bilingual `name`, `forms` (affirmative, negative and question, one or more formulas each), `uses` (Vietnamese and English description plus an original English example), `signals`, a bilingual `tip` on a common mistake, and three `practice` items. A practice item has a sentence with one ___, four options of which only one is grammatical, the answer and a Vietnamese explanation. The tutor indexes each tense under the `grammar` source type, with its English and Vietnamese names, so questions in either language find it.

## Tutor guide — guides.json

Generated by `python scripts/create-guides.py`. Fifty entries the AI tutor answers from when learners greet it, ask who it is, or ask about EnglishUp itself: greetings (9), about the app (8), the level test (8), learning paths (9), how each page works (10) and account and study habits (6). Fields: `id` (`g-<slug>`), `category`, bilingual `question` and `answer`, and `keywords`, other ways learners phrase the question, which help retrieval. The facts follow the app's real rules (README, `services/placement.ts`, `roadmaps.json`); when a rule changes, change the entry. Guides have no learner page; admins edit them under **Tutor guide**. Each guide and each learning path is one RAG chunk (source types `guide` and `roadmap`).
