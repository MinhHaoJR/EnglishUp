# Design system

Written from the built interface (2026-11-09) with the design-craft skill. Tokens live in `src/styles/theme.css`; `src/styles.css` is the older structural base underneath it.

## Direction

EnglishUp reads like bilingual wayfinding: each skill is a colour-coded line with its own pictogram, today's plan is a route of stops, and the next stop is always the most visible thing. It refuses both the candy-gamified learning dashboard and the KPI-tile admin board.

Chosen from seven candidates drawn from Vietnamese learners' world (guide signs, textbooks and highlighters, squared exercise books, timetables, Swiss poster grids, bilingual dictionaries, messaging apps) by the skill's roll, seed `5d3ea829/0`.

## Color

Strategy: full palette, one line per page (colour pass of 10/11/2026, design-craft colorize + layout). Each learning page owns its skill line at page scale: a 5% wash on the ground, a title plate with the page pictogram on a 17%→5% tint, line-tinted panel edges, primary buttons filled with the line, stat tiles, tabs, progress bars, checkboxes and choices. Signal yellow stays reserved for "you are here". CEFR levels have their own sequential spectrum (below), used for level chips and the faint wash of each lesson card. Vocabulary topic tiles walk the same spectrum with a coloured stop, so long lists read as varied but stay in one family. The Overview's title plate ends in a six-segment route map of the skill lines. Harmony comes from one recipe: tints are the line mixed into the panel at 4, 10, 17 and 24 percent, and text colours are the line mixed 78% with ink (`--line-wash`, `--line-tint`, `--line-edge`, `--line-text`). Earlier strategy, kept for the admin pages: neutrals plus sign blue, with line colours for skills only. Light is the default because learners mostly practise in daylit rooms. Dark is the night-lit sign, used on phones in the evening.

| Role                         | Light     | Dark      | Where it is used                                                                                   |
| ---------------------------- | --------- | --------- | -------------------------------------------------------------------------------------------------- |
| Ground `--bg`                | `#f3f6f9` | `#0d1828` | Page background                                                                                    |
| Surface `--panel`            | `#ffffff` | `#142338` | Panels, plates, inputs                                                                             |
| Text `--ink`                 | `#13243a` | `#e9eff6` | Body and headings: 15.7:1 on panel (light), 13.5:1 (dark)                                          |
| Secondary text `--muted`     | `#55677b` | `#a6b4c5` | Meta, captions: 5.8:1 on panel and 5.3:1 on ground (light), 7.5:1 (dark)                           |
| Border `--border`            | `#d8e0e9` | `#283a54` | 1px rules and plate edges                                                                          |
| Tint `--soft`                | `#eaf0f6` | `#1b2d47` | Hover, segmented tab track, chips                                                                  |
| Accent `--primary`           | `#0b5cad` | `#62a8f2` | Primary buttons, links, focus ring (light). White on it 6.7:1; dark text on the dark variant 6.8:1 |
| Accent tint `--primary-soft` | `#e3eefa` | `#18324f` | Active nav item, notices                                                                           |
| Signal `--signal`            | `#ffc629` | `#ffd44f` | "You are here" only: the active nav dot, the next route stop ring, today's week label. Never text  |
| Success `--success`          | `#136b40` | `#4cc787` | Right answers, finished plan. About 5.8:1 on its tint                                              |
| Danger `--danger`            | `#b42318` | `#ff8a7a` | Wrong answers, errors, destructive buttons. 5.75:1 (light) and 6.6:1 (dark) on its tint            |

The line colours were picked at similar weight so no skill shouts. White pictograms reach 4.5–6.7:1 on the light tiles; dark tiles use `#0b1726` pictograms.

| Line                                | Light     | Dark      |
| ----------------------------------- | --------- | --------- |
| Vocabulary                          | `#1a8754` | `#45c486` |
| Listening                           | `#6b47c9` | `#a68cf5` |
| Speaking                            | `#c2410c` | `#f2854c` |
| Reading                             | `#0e7490` | `#3fbcd8` |
| Writing                             | `#be185d` | `#ef6c9c` |
| Grammar (sentence patterns)         | `#a16207` | `#e2aa3f` |
| Overview (dashboard)                | `#0b5cad` | `#62a8f2` |
| Learning paths and level test       | `#4338ca` | `#8b93f5` |
| Games                               | `#a21caf` | `#e07ae6` |
| Achievements                        | `#be123c` | `#f7718d` |
| Services (tutor, settings, account) | `#3d5a80` | `#8aa6c8` |

CEFR spectrum (`--lv-a1` … `--lv-c2`), each with white text at 5:1 or more in light and dark ink in dark mode:

| Level | Light     | Dark      |
| ----- | --------- | --------- |
| A1    | `#15803d` | `#4ade80` |
| A2    | `#0f766e` | `#2dd4bf` |
| B1    | `#0369a1` | `#38bdf8` |
| B2    | `#4338ca` | `#8b93f5` |
| C1    | `#7e22ce` | `#c08af8` |
| C2    | `#be185d` | `#f472b6` |

`[data-skill]` sets `--line`, `--skill-accent` and `--skill-soft` (12% of the line colour over the panel). Legacy names `--green`, `--accent`, `--skill-*` point at these tokens for older stylesheets.

## Type

One family: Be Vietnam Pro, self-hosted through `@fontsource/be-vietnam-pro` (400, 400 italic, 500, 600, 700, 800). It covers every Vietnamese diacritic. Japanese and Chinese text lists Yu Gothic, Yu Mincho or Microsoft YaHei first.

| Role                          | Size                       | Weight | Line height | Tracking |
| ----------------------------- | -------------------------- | ------ | ----------- | -------- |
| Page title (h1)               | clamp(1.6rem, 2.2vw, 2rem) | 700    | 1.2         | -0.02em  |
| Section heading (h2)          | 1.25rem                    | 700    | inherited   | -0.01em  |
| Item heading (h3, list names) | 1rem                       | 700    | inherited   | 0        |
| Body                          | 1rem                       | 400    | 1.6         | 0        |
| Label                         | 0.875rem                   | 600    | inherited   | 0        |
| Meta and captions             | 0.8125rem                  | 400    | 1.4         | 0        |

Steps are at least 1.25× apart, from body to h2 to h1.

## Space

Base unit 4px. In use: 2 and 4 inside tight groups, 8 and 12 between related items, 16 and 24 between groups and panels, 32 and 48 at page edges. Panels pad 24px (18px on phones). Headings sit closer to what follows than to what precedes.

## Shape and elevation

- 16px (`--radius`): panels, lesson cards, route stops, chat window, notices.
- 12px (`--radius-sm`): buttons, inputs, selects, nav items, pictogram tiles, sign plates.
- 6px: small tiles, segmented tab buttons, week bars.
- Pill: only for small chips (badges, page meta, progress tracks, suggestion chips).

Panels inside the workspace float: 16px corners, a border tinted 8% toward primary and `--panel-shadow` (a soft drop that deepens in dark mode), after the owner's dashboard reference. Other controls keep a 1px `--border` and no shadow, apart from the exceptions below.

The Settings look applies everywhere: every page title has a one-line subtitle; selects draw their own primary chevron; fields gain a primary-tinted edge on hover and a primary border with a soft 3px ring on keyboard focus; ticks and radios are 18px; notices are soft tip cards (9% primary on the panel, 16px corners).

Behind every page sit soft waves (lower left, right side, a faint arc at the top) and a dot grid fading from the top-right corner. Both are masks over the primary colour (`public/bg/waves.svg`), so they follow light and dark; they ignore the pointer, sit under content, drop the dots below 700px and disappear in print. The overview is denser to fit one screen: 18px gaps and panel padding, a 1.625rem title on a white-to-wash plate with a 4px route line, 56px route stops and 32px skill tiles.

## Motion

120ms ease-out on button and border colours. The tutor's typing dots are the only animation. `prefers-reduced-motion` turns off all transitions and animations.

## Components

- **Sidebar directory.** Three groups: home, the six skill lines, then services, split by 1px rules. Each item has a 30px pictogram tile in its line colour. The active item gets the blue tint, bold text and the yellow dot. Never use a coloured side stripe. On phones it becomes a horizontal row, and the dot becomes a 3px yellow underline.
- **Page title.** The h1, then an optional `page-meta` chip for facts such as level and topic, then an optional one-line description. There is no eyebrow above the heading.
- **Route (home).** Stops are joined by their line colour; a stop is solid once done, and the next stop has the yellow ring and `aria-current="step"`. One primary "Start" button sits at the end. On phones the route runs vertically.
- **Line list.** A tile, the name with a fact line, an optional score, then an arrow. It is used for the skill directory, the topic list and the starter lessons. Rows divide with 1px rules, never cards.
- **Sign plate.** A small bordered status sign (streak, minutes today). It is not a hero metric.
- **Stats.** One compact row of small plates (number 1.5rem). Never a 2×2 wall of big numbers.
- **Lesson cards.** The level and topic badge is tinted with the page's line. The card button is secondary (outline) so one primary action remains per screen.
- **Segmented tabs.** A tinted track with the selected tab raised on the panel colour.
- **Choice grid.** Right and wrong answers are marked by colour and also by ✓/✗ plus a status message.
- **Vocabulary study** (`src/styles/vocabulary-study.css`, surface roll seed `31f64b64/0`, layout #2 of 7, "diptych" composition). The practice tab shows the current topic as one bar (name, word count, level, Change topic). The topic directory opens only before a topic is chosen or on request.
  - Each 20-word group is a station on the topic's line. Station states are empty, half-filled or solid; the selected station gets the yellow ring.
  - Two piles always sit side by side: "To learn" and "Remembered" (reviewed with repetitions > 0).
  - Four large mode tiles (radio group) and one primary Start button.
  - The card puts one word large and centred. The answer box is tinted right or wrong.
  - Four rating buttons pair colour with their word and keys 1–4. Space reveals.
  - Key hints are hidden on touch screens and below 700px. The totals hide while a card is on screen.
- **Lesson pages** for reading, listening, speaking and writing (surface roll seed `a9c0e33c/0`: layout #4 of 7, one question at a time, "marginalia" composition).
  - `.split` puts the material in a primary column (text capped at 68ch) beside a 300–380px rail that stays in view while you scroll.
  - The rail stacks under the material below 960px.
  - Questions come one at a time. Numbered stations are blue when answered and green or red once checked; the current one has the yellow ring.
  - Answer choices are 48px rows.
  - Lesson lists on these four pages are directory rows: level chip, title, one-line excerpt and facts, with the action on the right.
- **Icons.** Play, stop, download and upload are drawn in the shared icon set; no glyph icons remain on learning screens.
- **Tutor.** A round chat head in the corner opens a messaging window: header with avatar and status, bubbles on both sides, source chips and a rounded composer.
- **Account page** (`/account`). It follows the user's reference, a classic account-settings layout, played straight in this world.
  - Left: a profile card with a sign-blue cover (dimmed at night), a 92px yellow monogram, the display name, the email and "View achievements".
  - Under the card, a section menu styled like the sidebar directory: service tile, label and chevron. The current section gets the blue tint, bold text and the yellow dot. "Sign out" is the last row, in danger colours.
  - Right: one pane at a time, chosen by `?tab=`:
    - Profile: read-only email, display name, leaderboard opt-in with a live yellow preview row.
    - Points & sync: a sign-blue score plate with tabular numerals and a signal-yellow meter, plus a sync bar.
    - Learning journey: the last ten active days as route stops in skill-line colours, badge days in yellow.
    - Change password: current, new with the live rule list, repeat. Uses Identity's `POST /api/manage/info`.
    - Privacy: one row per kind of data.
  - Sections the product does not have (notifications, photos, delete account) are left out.
  - Below 860px the card turns horizontal and the menu becomes a sideways row.
- **Admin page** (`/admin`, admins only, surface roll seed `27a71f5c/0`: structure #3 of 6, control room, "timeline as spine" composition).
  - Presence comes first: big tabular counts for online (green go-light) and offline, a green split bar, the refresh time, the two-minute rule and a Refresh button.
  - "Today" follows as one ruled row of four counts (opened the app, practices, tutor questions, races) with a line of system totals.
  - Users hang on one line ordered by when they were last seen, in bands: online now, today, last 7 days, earlier, never seen. Each account is a stop with its light, email, display name, tags (Admin, Locked, On leaderboard), points, practices, last seen and actions. The admin's own row is lit yellow and cannot be locked.
  - Locking takes a second click to confirm. The page refreshes every 30 s.
  - It is a separate page outside the learning shell, with no sidebar or tutor bubble. Its own sticky sign-blue bar carries the brand, a yellow "Admin" plate, the admin's email, "Learning app" and "Sign out". Signing in with an admin account lands here. A learner opening `/admin` is sent to the learning app, and a signed-out visitor to sign-in.
  - In the learning app, the sidebar shows an extra "Admin" group only for admins.
  - The bar has two areas, Overview and Learning content; the current one is underlined in signal yellow.
  - Learning content has nine kind tabs, each tinted with its skill line, and a search plus "+ Add" toolbar. Each item shows its title, id, level and a status chip: Live (grey), Hidden (yellow) or Invalid (red). Actions are Edit, Hide or Show, and Delete, which asks for a second click. Every item is listed, with no paging, in collapsible bars in the learning pages' order. Sentence patterns are grouped by grammar group (the grammar page's 12 groups), synonym/antonym entries by level, and every other kind by topic in catalog order. Each bar shows its item count. Opening a vocabulary topic shows the same 20-word clusters learners study (cluster headings in the vocabulary green); other kinds open to one list. Hidden or invalid items follow under their own heading. "Expand all" and "Collapse all" sit above the bars, and a search opens every group that has a match while keeping each word's real cluster number.
  - Colour pass (design-craft colorize + layout, full palette of the skill lines, each with a job): the chosen kind's line colour tints the header band behind the title and tabs, fills the selected tab, tints the group bars and their count chips, and fills the cluster headings. Item rows sit on alternating soft grounds with a skill-tinted hover instead of hairlines. The id and level are small chips in the kind's colour. Status chips carry a dot and a word in the inherited semantic colours: Live green, Hidden yellow, Invalid red. Actions carry icons: Edit is the only tinted action (sign blue); Delete and Lock account are red outlines. In the item form, repeated blocks and their numbered legends use the kind's colour.
  - Overview: each section heading has a sign-blue icon tile. The four "today" figures are tinted tiles, each keeping one line colour (opened the app teal, practices green, tutor questions purple, races orange). User rows alternate on soft grounds, with a fixed-width actions column so the columns line up, and the admin's own row stays yellow.
  - The editor is a two-column form for every kind, built from a field list per kind (`ContentForm.tsx`). Long texts, lists (one entry per line) and repeated rows span both columns. Dialogue lines and questions are tinted blocks with their own Remove button and an "+ Add item" button below. A reading passage gets a tall box. A live list names each problem once, in form order, as "field: what is wrong" in the interface language (for example "Câu hỏi 3 › Đáp án chấp nhận: chưa điền" or "Số từ tối đa: phải lớn hơn 0"). It shows the first eight, then a count. A rule on a whole question waits until that question's fields are filled. A new synonym entry takes its id from its level and headword (`rel-b2-big`), and an id already in the library is refused, and "Save to the database" stays disabled until there are none.
- **Tutor page** (`/assistant`, Tutor Tom's room, after the owner's reference image). A 300px rail and a stage, 20px apart, filling the viewport.
  - The rail is a 24px card on a faint primary wash: Tom's card (avatar in a primary ring with the presence dot, name, status), a pill "New conversation", then Today / Earlier (clock and history icons) as the only scrolling part. Each chat row has a bubble icon in a white disc, a two-line title and the time; the open one sits on the soft fill, and delete shows on hover, on focus and on the open row. A London skyline, a mask over the primary colour so it reads in both themes, fills the rail's foot.
  - The stage starts with a strip of sky (fixed light gradient in both themes, like Tom's artwork): Tom peeks over the card edge with his paws on it, a tilted white speech bubble says "English made easy!", and the name sits large with the status, among white paw prints. The chat card hangs under it with 24px lower corners.
  - The card opens with a soft bar (megaphone for a new chat, bubble for an open one, the subtitle and questions left today), then a centred 860px reading column: answers as plain text beside Tom's avatar, questions as blue bubbles, sources by skill line.
  - An empty chat shows a yellow sparkle with "What would you like to ask today?" and four starter cards in two columns, each with a 52px skill-line tile, the skill name, the question and a chevron.
  - The composer is the corner chat's pill (sparkle and divider) beside a 56px round send button; the footnote with a small shield reminds that answers can be wrong.
  - Once a chat has messages the sky folds away and the card takes the full height, with 24px corners all round.
  - Below 1100px the speech bubble goes; below 860px the rail becomes a sideways strip of the new-chat pill and chats, and the sky shrinks to a 118px Tom beside the name.
- **Sign-in entrance** (`/login`, `src/features/account/SignIn.tsx`). A full-screen page outside the app shell: no sidebar, top bar or tutor bubble.
  - Left is a sign-blue plate (`--plate`): brand, one h1, and what an account adds as an upright three-stop route with white pictogram tiles.
  - Right is the form: segmented Sign in / Create account, email, password with a drawn eye toggle, a live checklist of the server's password rules while creating an account, one full-width primary button, a privacy line and a "Keep practising without an account" link.
  - At night the plate dims to `--primary-soft` with ink text instead of a bright panel. Below 860px the plate stacks above the form.
  - Every sign-in link carries `?next=` back to the page that asked. Only same-site paths are followed. Signed-in visitors skip the page. `/account` sends signed-out visitors here.
- **Games** (`/game`). Two race cards side by side as tabs, each in its skill line (vocabulary green, grammar amber); the chosen one is tinted and outlined. In the grammar race the sentence is centred at reading size and the blank is a tinted box with a line underneath; after an answer the box holds the right option, and a wrong answer adds the Vietnamese explanation under the options. The leaderboard lists ranks on alternating soft rows, with gold, silver and bronze plates for the top three, games played and a blue best-score chip; the learner's own row is yellow.
- **Level test** (`/placement`). One question at a time with a progress bar, and the same blank box for grammar. The result pairs the score tile (sign blue) with the estimated level (grammar amber), then one bar per level, green when passed, and a button to the matching path.
- **Learning paths** (`/roadmap`). A five-step level ladder (the current path filled sign blue, "Following" or "Suggested" under it), a head with the summary, fact chips and a progress tile, then the stages as numbered stops on one vertical line, green with a check when complete. Tasks are rows tinted in their skill line with a checkbox, a pictogram tile, the page and level, and an "Open" button.

- **Grammar** (`/grammar`). Under the title plate, two part cards in the grammar line: Sentence patterns and Tenses (`?part=tenses`). Tenses open on a three-column timeline. Past is indigo, present teal and future pink, the same family as the CEFR spectrum. Each column is a tinted plate of tense buttons, and the chosen one is filled in its time colour. The tense card keeps that colour. It shows a level chip and a time chip, the heading, and the forms as three rows with round +/−/? signs and formula chips. Then come numbered uses with speakable examples, signal-word pills, a yellow-washed tip and the quick check, which uses the race's blank box. Below 860px the timeline stacks and each column shows two tenses a row.

- **Lesson lists** (reading, listening, speaking, writing; `LessonBrowser`). One shared list under the title plate. A seven-step level band (All, A1–C2) walks the CEFR spectrum: each step is tinted in its level colour and shows "done/total" with a thin meter, and the chosen step is filled. Below 860px the band wraps to four columns and keeps only the count. A tool row washed in the page's line colour holds the topic picker (only topics the list has), title search, a "not done yet" switch and a filled "Next lesson" button for the first unfinished lesson. Cards sit in an auto-fill grid (260px minimum), each washed from the top in its level colour, with level and topic chips, a green score pill once done, a two-line preview, a meta line and a start button whose hit area covers the card. Twelve cards show at first; "Show more" adds twelve. Done means a saved attempt whose label is the lesson title (dictation: its id).
- **Tutor Tom** (corner chat window, `ChatWidget` with `Chat`). 400 × 680px, 24px radius. The header is a soft primary gradient with a curved lower edge: Tom's round avatar in a primary ring with a green presence dot, the name in 18px bold over the status, and round white tool buttons (new chat, open the page, minimize, close) with primary icons. An empty chat (the welcome goes as soon as a question is sent) shows Tom on a fixed light stage (#f6fafd, the colour of his artwork, in both themes) with two sparkles and a paw print, an intro card on the soft fill and three full-width pill suggestions (1.5px primary edge, icon, text, chevron). The composer is a pill with a sparkle and a divider beside a 52px round primary send button; the footnote carries a small shield. Under 420px the tool buttons shrink to 32px and the name and status stay on one line. The full tutor page keeps its boxed composer and shows Tom's avatar beside answers.
- **Vocabulary** (after the owner's reference). The title plate adds a tilted slogan ("Learn every day, build your future") with a paper plane and a stack of books with a mortarboard. Four stat cards each take a tint (blue new, green learning, orange mastered, purple accuracy) with a sign, the number and a picture on the right; accuracy shows a ring filled to its value. Tabs are pills with signs, the current one filled in primary with a yellow bolt. The topic bar sits between an open book and a rising chart, its name beside a star. The directory heading has a bookmark; groups are pills with signs (flame, briefcase, mortarboard, trophy, page); topic cards cycle green, blue, purple and pink with a white chevron disc. Pictures are cut from the reference and dim slightly in dark mode; below 860px they and the stat pictures go.
- **Word group chooser** (vocabulary practice, after the owner's reference). The heading has a mortarboard and a yellow highlighter underline, with the group count in a pill. Groups are station cards on a green line (hollow, half and full dots), the chosen one raised with the yellow ring; counts sit in small pills. "To learn" lists words as soft chips; "Remembered" is a green card with a white tick on a green disc and a reading robot. Practice modes are tall cards, the chosen one filled in a primary gradient. Start is a green pill with a tick; next group a white pill with a mortarboard. A stack of books sits in the corner above 1100px; pictures are cut from the reference.
- **Account profile** (after the owner's reference). The page has no title plate (a hidden heading keeps it for screen readers); the side and the pane run the same height in every section, and the privacy rows centre their text on a soft sign tile. The profile card has a primary gradient cover with white laurel sprigs curving into the panel, a yellow monogram with a green verified tick, the email beside a mail sign and a soft pill "View achievements" with a chart sign. Menu rows are separate soft cards with coloured pictograms (blue home, sync and shield; orange flame; navy lock) and primary chevrons; the current one sits on the primary fill and sign out on the danger fill. The pane head pairs a 1.75rem title with a green "Active" pill. The profile form sits beside an ID-card illustration cut from the reference, with mail and mortarboard signs on its labels, an info sign on the hint, 14px fields on a faint primary fill, the leaderboard preview on a soft card and a 52px pill save button with a save sign. Below 860px the illustration goes and the card and menu return to the compact row and sideways strip.
- **Settings** (after the owner's reference). The title plate adds "Tune how you study". One card holds two columns of fields; each label has a primary pictogram (globe, gauge, target, speaker, palette). Selects are 12px boxes with a sign inside on the left: the drawn flag of the interface language or accent (`Flag`, shared with the language picker), or a sun or moon for the theme; the daily goal has a clock on the right. The speech rate slider fills to its value in primary with a white-ringed thumb. A tip on the soft fill pairs a yellow bulb with a small rising chart. The data card puts a shield tile beside its heading, icons on its three buttons and, above 860px, an illustration of a shield, cloud and database cut from the reference.
- **Learning language picker** (sidebar). A select-only combobox (WAI-ARIA): the heading "Learning" sits beside a filled globe disc and a fading hairline; the pill (2px primary edge, white-to-wash fill, 999px radius) shows a drawn flag, a thin divider, the name over its native form, and a chevron in a soft primary disc that turns up while open. The list opens under it as a 16px-radius card with a notch pointing back at the pill; rows carry the same flag and divider, the current language sits on the soft fill with a primary check disc, and the row under the pointer or arrow keys gets a thin primary outline. Arrow keys, Home, End, Enter, Space, Escape and Tab work as in the pattern; a click outside closes it. Flags are inline SVG on a 30 × 20 grid, not emoji.
- **Lesson sessions** (reading, listening, speaking, writing, level test). Two columns at 1.3 : 1 above 960px, one below. The left column stacks separate cards for the material (passage; audio then transcript; model text then recorder; task then the writing desk), the right holds the task. Questions (`Questions`) show "Question n/total" in the line colour with the answered count, the station row, the prompt at 19px bold, then answers as full-width rows with a lettered disc (A, B, C); the native radio stays in the row for keyboard and screen readers and the row carries the focus ring. The check button sits under the questions, full width, disabled until every question has an answer, with a count of what is left; once checked, the right answer turns green and a wrong pick red. The writing desk is its own card washed in the line colour around a white sheet, with the timer and save state above it and a word meter (green inside the range, red past it) beside the submit button. Checklists are bordered rows that fill with the line tint when ticked. The level test intro puts how it works beside a start box; its questions read as one centred 760px column with lettered answers.

## Deliberate exceptions

- `.study-card > h2:focus { outline: none }`: the word heading is focused by code so screen readers announce each new card (`craft-ignore`).
- `main:focus { outline: none }`: `main` receives focus from code on every route change, for screen readers. It is not a control, and every control keeps the focus ring (`craft-ignore` in `theme.css`).
- The floating tutor (chat head and window) uses `--shadow-float`, because it really sits above scrolling content.
- The selected segmented tab has a 1px shadow to lift it out of its track.
- Sentence-pattern cards keep their number (#1–#100), because it refers to the reference list.

## Out of system

- `src/styles/vibrant-languages.css` still hard-codes colours for the Japanese/Chinese practice screens and their dark variants; those screens have not been reviewed against the theme.
- Some Japanese/Chinese topic marks in the data are arrows or symbols (`↗`, `⌂`) rather than drawn icons.
- There is no authored motion moment yet. The route filling in as stops are completed is the obvious candidate.
