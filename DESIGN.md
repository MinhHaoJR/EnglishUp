# Design system

Written from the built interface (2026-11-09) with the design-craft skill. Tokens live in `src/styles/theme.css`; `src/styles.css` is the older structural base underneath it.

## Direction

EnglishUp reads like bilingual wayfinding: each skill is a colour-coded line with its own pictogram, today's plan is a route of stops, and the next stop is always the most visible thing. It refuses both the candy-gamified learning dashboard and the KPI-tile admin board.

Chosen from seven candidates drawn from Vietnamese learners' world (guide signs, textbooks and highlighters, squared exercise books, timetables, Swiss poster grids, bilingual dictionaries, messaging apps) by the skill's roll, seed `5d3ea829/0`.

## Color

Strategy: restrained. Neutrals plus one accent (sign blue), with signal yellow reserved for "you are here", and six line colours used only to identify skills (pictogram tiles, route segments, tints). Light is the default because learners mostly practise in daylit rooms. Dark is the night-lit sign, used on phones in the evening.

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

| Line                                                 | Light     | Dark      |
| ---------------------------------------------------- | --------- | --------- |
| Vocabulary                                           | `#1a8754` | `#45c486` |
| Listening                                            | `#6b47c9` | `#a68cf5` |
| Speaking                                             | `#c2410c` | `#f2854c` |
| Reading                                              | `#0e7490` | `#3fbcd8` |
| Writing                                              | `#be185d` | `#ef6c9c` |
| Grammar (sentence patterns)                          | `#a16207` | `#e2aa3f` |
| Services (home, tutor, race, achievements, settings) | `#3d5a80` | `#8aa6c8` |

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

- 12px (`--radius`): panels, lesson cards, route stops, chat window.
- 8px (`--radius-sm`): buttons, inputs, nav items, pictogram tiles, sign plates.
- 6px: small tiles, segmented tab buttons, week bars.
- Pill: only for small chips (badges, page meta, progress tracks, suggestion chips).

Elevation is a 1px `--border` and nothing else. Shadows are not combined with borders, apart from the exceptions below.

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
  - The sidebar shows an extra "Admin" group only for admins.
- **Tutor page** (`/assistant`, surface roll seed `66dcd42e/0`: structure #1 of 6, workspace with history rail, "contact sheet" composition). It is one 12px plate filling the viewport.
  - The rail lists saved chats as small frames grouped Today / Earlier, with title and time. The open frame grows, gets a blue border and the yellow "you are here" dot. Delete shows on hover, on focus or for the open frame.
  - The main frame has a header (open title, status, questions left today) and a centred 760px reading column. Answers read as plain text beside the avatar, questions are blue bubbles, and sources are labels with the skill-line tile.
  - An empty frame asks "What would you like to ask today?" and offers four starter questions, one per skill line.
  - The composer is a bordered box whose border shows focus, with a filled send button. One footnote covers accuracy and privacy.
  - Below 860px the rail becomes a sideways strip of frames.
  - The corner chat keeps its messenger window, and both share `ChatPanel`.
- **Sign-in entrance** (`/login`, `src/features/account/SignIn.tsx`). A full-screen page outside the app shell: no sidebar, top bar or tutor bubble.
  - Left is a sign-blue plate (`--plate`): brand, one h1, and what an account adds as an upright three-stop route with white pictogram tiles.
  - Right is the form: segmented Sign in / Create account, email, password with a drawn eye toggle, a live checklist of the server's password rules while creating an account, one full-width primary button, a privacy line and a "Keep practising without an account" link.
  - At night the plate dims to `--primary-soft` with ink text instead of a bright panel. Below 860px the plate stacks above the form.
  - Every sign-in link carries `?next=` back to the page that asked. Only same-site paths are followed. Signed-in visitors skip the page. `/account` sends signed-out visitors here.

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
