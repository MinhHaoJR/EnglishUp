import { useEffect, useRef, useState } from 'react';
import type { Word } from '../../data/schema';
import { useBi, useT, topicVi } from '../../i18n';
import { Notice, useLive } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { db } from '../../services/storage';
import { stopSpeech } from '../../services/speech';
import type { Rating } from '../../services/srs';
import {
  advanceStudyWord,
  beginStudyGroup,
  selectStudyGroup,
  selectedStudyGroup,
  studyGroups,
  visitedWords,
} from '../../services/vocabularyStudy';
import '../../styles/vocabulary-study.css';

type Mode = 'flashcards' | 'choice' | 'type' | 'spell';
const modes: [Mode, IconName, string, string][] = [
  ['flashcards', 'cards', 'Thẻ ghi nhớ', 'Flashcards'],
  ['choice', 'choice', 'Chọn nghĩa đúng', 'Multiple choice'],
  ['type', 'keyboard', 'Gõ từ tiếng Anh', 'Type the word'],
  ['spell', 'speaker', 'Nghe và viết từ', 'Listen and spell'],
];
const ratings = ['again', 'hard', 'good', 'easy'] as const;
/** Lets keyboard shortcuts ignore keys typed into a field. */
const typing = (target: EventTarget | null) =>
  target instanceof HTMLElement && !!target.closest('input, textarea, select');
export default function VocabularyPractice({
  words,
  all,
  scope,
  ready,
  onActiveChange,
}: {
  words: Word[];
  all: Word[];
  scope: string;
  ready: boolean;
  onActiveChange: (active: boolean) => void;
}) {
  const bi = useBi();
  const t = useT();
  const { value: saved, error: readError } = useLive(
    async () => ({
      progress: await db.vocabularyStudy.get(scope),
      reviews: await db.reviews.toArray(),
    }),
    [scope],
  );
  const [mode, setMode] = useState<Mode>('flashcards');
  const [queue, setQueue] = useState<Word[]>([]);
  const [index, setIndex] = useState(0);
  const [sessionGroup, setSessionGroup] = useState('');
  const [answer, setAnswer] = useState('');
  const [revealed, setRevealed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [finished, setFinished] = useState(false);
  const [rated, setRated] = useState(0);
  const [skipped, setSkipped] = useState(0);
  const saving = useRef(false);
  const started = useRef(0);
  const heading = useRef<HTMLHeadingElement>(null);
  const chooser = useRef<HTMLHeadingElement>(null);
  const groups = studyGroups(words);
  const visited = visitedWords(words, saved?.progress, saved?.reviews ?? []);
  const selected = selectedStudyGroup(words, saved?.progress, saved?.reviews ?? []);
  const remaining = selected?.words.filter((word) => !visited.has(word.id)) ?? [];
  const nextGroup = groups.find(
    (group) => group.id !== selected?.id && group.words.some((word) => !visited.has(word.id)),
  );
  const remembered = new Set(
    (saved?.reviews ?? []).filter((review) => review.repetitions > 0).map((review) => review.id),
  );
  const card = queue[index];
  const activeGroup = groups.find((group) => group.id === sessionGroup);
  const matched =
    card &&
    (mode === 'choice'
      ? answer === card.id
      : answer.trim().toLowerCase() === card.word.toLowerCase());
  const options = card
    ? [
        card,
        ...all
          .filter((word) => word.id !== card.id && word.meaning !== card.meaning)
          .slice(index % 20, (index % 20) + 3),
      ].sort((a, b) => a.meaning.localeCompare(b.meaning))
    : [];
  useEffect(() => {
    onActiveChange(!!card);
    heading.current?.focus();
    if (!card && finished) chooser.current?.focus();
    stopSpeech();
  }, [card, finished, onActiveChange]);
  useEffect(
    () => () => {
      onActiveChange(false);
      stopSpeech();
    },
    [onActiveChange],
  );

  async function run(action: () => Promise<void>) {
    if (saving.current) return;
    saving.current = true;
    setBusy(true);
    setError(false);
    try {
      await action();
    } catch {
      setError(true);
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }
  function start(groupId = selected?.id, replay = remaining.length === 0) {
    if (!groupId) return;
    void run(async () => {
      const next = await beginStudyGroup(scope, words, groupId, replay);
      if (!next.length) return;
      setQueue(next);
      setSessionGroup(groupId);
      setIndex(0);
      setAnswer('');
      setRevealed(false);
      setFinished(false);
      setRated(0);
      setSkipped(0);
      started.current = Date.now();
    });
  }
  function advance(rating?: Rating) {
    if (!card) return;
    void run(async () => {
      await advanceStudyWord(scope, sessionGroup, card, started.current, rating);
      if (rating) setRated((value) => value + 1);
      else setSkipped((value) => value + 1);
      setIndex((value) => value + 1);
      setAnswer('');
      setRevealed(false);
      started.current = Date.now();
      if (index + 1 === queue.length) setFinished(true);
    });
  }
  useEffect(() => {
    if (!card) return;
    const onKey = (event: KeyboardEvent) => {
      if (typing(event.target) || busy) return;
      if (!revealed && mode === 'flashcards' && (event.key === ' ' || event.key === 'Enter')) {
        event.preventDefault();
        setRevealed(true);
      } else if (revealed && /^[1-4]$/.test(event.key)) {
        const rating = ratings[Number(event.key) - 1];
        if (mode === 'flashcards' || matched || rating === 'again') advance(rating);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });
  const notices = (
    <>
      {readError && <Notice error>{readError}</Notice>}
      {error && (
        <Notice error>
          {bi(
            'Chưa lưu được tiến độ. Hãy thử lại; thẻ hiện tại vẫn được giữ nguyên.',
            'Could not save progress. Please retry; your current card is unchanged.',
          )}
        </Notice>
      )}
    </>
  );

  const piles = (group: (typeof groups)[number]) => {
    const todo = group.words.filter((word) => !remembered.has(word.id));
    const done = group.words.filter((word) => remembered.has(word.id));
    return { todo, done };
  };

  if (card) {
    const counts = activeGroup ? piles(activeGroup) : { todo: queue, done: [] };
    return (
      <section
        className="panel vocabulary-study study-session"
        aria-label={bi('Thẻ từ', 'Word card')}
      >
        {notices}
        <div className="study-topbar">
          <div className="pile-counters" aria-live="polite">
            <span className="pile-count todo">
              {bi('Cần học', 'To learn')} <strong>{counts.todo.length}</strong>
            </span>
            <span className="pile-count done">
              {bi('Đã nhớ', 'Remembered')} <strong>{counts.done.length}</strong>
            </span>
          </div>
          <button
            className="quiet"
            disabled={busy}
            onClick={() => {
              setQueue([]);
              setFinished(false);
              requestAnimationFrame(() => chooser.current?.focus());
            }}
          >
            {bi('Kết thúc sớm (giữ tiến độ)', 'End early (keep progress)')}
          </button>
        </div>
        <progress
          value={activeGroup?.words.filter((word) => visited.has(word.id)).length ?? index}
          max={activeGroup?.words.length ?? queue.length}
          aria-label={t('progress')}
        />
        <div className="study-card">
          <p className="study-card-meta">
            <span className="badge">
              {card.level} · {bi(topicVi[card.topic] ?? card.topic, card.topic)}
            </span>
            <span>
              {bi('Cụm', 'Group')} {activeGroup?.number} ·{' '}
              {(activeGroup?.words.findIndex((word) => word.id === card.id) ?? index) + 1}/
              {activeGroup?.words.length ?? queue.length}
            </span>
          </p>
          <h2 ref={heading} tabIndex={-1} lang={mode === 'type' ? undefined : 'en'}>
            {mode === 'spell'
              ? bi('Nghe và viết từ', 'Listen and spell')
              : mode === 'type'
                ? card.meaning
                : card.word}
          </h2>
          {mode === 'type' ? (
            <p className="study-hint">{card.definition}</p>
          ) : (
            <div className="study-sound">
              {mode !== 'spell' && (
                <span className="muted">{`${card.ipa ? `${card.ipa} · ` : ''}${card.pos}`}</span>
              )}
              <SpeakButton text={card.word} />
            </div>
          )}
          <fieldset disabled={busy}>
            <legend className="sr-only">{bi('Trả lời thẻ từ', 'Answer the word card')}</legend>
            {mode === 'choice' && !revealed && (
              <div className="choice-grid">
                {options.map((option) => (
                  <button
                    key={option.id}
                    aria-pressed={answer === option.id}
                    className={answer === option.id ? 'selected' : ''}
                    onClick={() => setAnswer(option.id)}
                  >
                    {option.meaning}
                  </button>
                ))}
              </div>
            )}
            {(mode === 'type' || mode === 'spell') && !revealed && (
              <form
                className="study-answer"
                onSubmit={(event) => {
                  event.preventDefault();
                  if (answer.trim()) setRevealed(true);
                }}
              >
                <label>
                  {t('answer')}
                  <input
                    autoComplete="off"
                    autoCapitalize="off"
                    spellCheck={false}
                    lang="en"
                    value={answer}
                    onChange={(event) => setAnswer(event.target.value)}
                  />
                </label>
                <button className="primary" disabled={!answer.trim()}>
                  {t('check')}
                </button>
              </form>
            )}
            {revealed ? (
              <>
                <div
                  className={`answer-box ${mode === 'flashcards' ? '' : matched ? 'right' : 'wrong'}`}
                >
                  {mode !== 'flashcards' && (
                    <strong>{matched ? t('correct') : bi('Đáp án đúng', 'Correct answer')}</strong>
                  )}
                  <h3>
                    <span lang="en">{card.word}</span> — {card.meaning}
                  </h3>
                  <p lang="en">{card.definition}</p>
                  {card.examples.map((example) => (
                    <p key={example} lang="en">
                      <em>{example}</em>
                    </p>
                  ))}
                </div>
                <p className="rating-question">
                  {bi('Bạn nhớ từ này tốt đến đâu?', 'How well did you remember?')}
                </p>
                <div className="rating-row">
                  {ratings.map((rating, i) => (
                    <button
                      key={rating}
                      className={`rating ${rating}`}
                      aria-keyshortcuts={String(i + 1)}
                      disabled={mode !== 'flashcards' && !matched && rating !== 'again'}
                      onClick={() => advance(rating)}
                    >
                      <kbd aria-hidden="true">{i + 1}</kbd>
                      {t(rating)}
                    </button>
                  ))}
                </div>
              </>
            ) : mode === 'flashcards' ? (
              <button
                className="primary study-main"
                aria-keyshortcuts="Space"
                onClick={() => setRevealed(true)}
              >
                {t('reveal')}
              </button>
            ) : mode === 'choice' ? (
              <button
                className="primary study-main"
                disabled={!answer}
                onClick={() => setRevealed(true)}
              >
                {t('check')}
              </button>
            ) : null}
          </fieldset>
        </div>
        <div className="study-footer">
          <button disabled={busy} className="quiet" onClick={() => advance()}>
            {bi('Bỏ qua / Tiếp tục →', 'Skip word →')}
          </button>
          <span className="muted keys-hint" aria-hidden="true">
            {mode === 'flashcards'
              ? bi('Phím cách: xem đáp án · 1–4: đánh giá', 'Space: reveal · 1–4: rate')
              : bi('1–4: đánh giá', '1–4: rate')}
          </span>
        </div>
      </section>
    );
  }

  const selectedPiles = selected ? piles(selected) : { todo: [], done: [] };
  return (
    <div className="vocabulary-study">
      {notices}
      <section className="panel study-chooser" aria-labelledby="study-title">
        <div className="panel-head">
          <h2 id="study-title" ref={chooser} tabIndex={-1}>
            <SkillIcon skill="cap" size={28} />
            <span>{finished ? t('result') : bi('Chọn cụm từ để học', 'Choose a word group')}</span>
          </h2>
          {selected && (
            <span className="study-count">
              <SkillIcon skill="chart" size={18} />
              {bi(
                `${groups.length} cụm · tối đa 20 từ`,
                `${groups.length} groups · up to 20 words`,
              )}
            </span>
          )}
        </div>
        {finished && (
          <Notice>
            {bi(
              `Lượt này: ${rated} từ đã đánh giá, ${skipped} từ bỏ qua.`,
              `This session: ${rated} rated, ${skipped} skipped.`,
            )}
          </Notice>
        )}
        {selected ? (
          <>
            <div
              className="station-line"
              role="radiogroup"
              aria-label={bi('Cụm từ vựng', 'Word group')}
            >
              {groups.map((group) => {
                const seen = group.words.filter((word) => visited.has(word.id)).length;
                const state = seen === group.words.length ? 'done' : seen > 0 ? 'started' : 'fresh';
                return (
                  <button
                    key={group.id}
                    role="radio"
                    aria-checked={group.id === selected.id}
                    aria-label={bi(
                      `Cụm ${group.number}, ${seen}/${group.words.length} đã đi qua`,
                      `Group ${group.number}, ${seen}/${group.words.length} visited`,
                    )}
                    className={`station ${state}`}
                    disabled={busy || !ready || !saved}
                    onClick={() =>
                      void run(async () => {
                        await selectStudyGroup(scope, words, group.id);
                        setFinished(false);
                      })
                    }
                  >
                    <span className="station-dot" aria-hidden="true" />
                    <span className="station-name">
                      {bi('Cụm', 'Group')} {group.number}
                    </span>
                    <small>
                      {seen}/{group.words.length}
                    </small>
                  </button>
                );
              })}
            </div>

            <div className="diptych">
              <section className="pile todo" aria-labelledby="pile-todo">
                <h3 id="pile-todo">
                  <SkillIcon skill="reading" size={22} />
                  {bi('Cần học', 'To learn')} <span>{selectedPiles.todo.length}</span>
                </h3>
                {selectedPiles.todo.length ? (
                  <ul>
                    {selectedPiles.todo.map((word) => (
                      <li
                        key={word.id}
                        lang="en"
                        className={visited.has(word.id) ? 'seen' : undefined}
                      >
                        {word.word}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted">
                    {bi('Bạn đã nhớ hết cụm này.', 'You remember this whole group.')}
                  </p>
                )}
              </section>
              <section className="pile done" aria-labelledby="pile-done">
                <h3 id="pile-done">
                  <span className="pile-tick" aria-hidden="true">
                    <SkillIcon skill="check" size={16} />
                  </span>
                  {bi('Đã nhớ', 'Remembered')} <span>{selectedPiles.done.length}</span>
                </h3>
                {selectedPiles.done.length ? (
                  <ul>
                    {selectedPiles.done.map((word) => (
                      <li key={word.id} lang="en">
                        {word.word}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted">
                    {bi(
                      'Từ chọn “Nhớ được” hoặc “Dễ” sẽ chuyển sang đây.',
                      'Words you rate Good or Easy move here.',
                    )}
                  </p>
                )}
                <img
                  className="pile-art"
                  src="/art/study-robot.webp"
                  width={220}
                  height={275}
                  alt=""
                  draggable={false}
                />
              </section>
            </div>

            <div
              className="mode-tiles"
              role="radiogroup"
              aria-label={bi('Cách luyện tập', 'Practice mode')}
            >
              {modes.map(([value, icon, vi, en]) => (
                <button
                  key={value}
                  role="radio"
                  aria-checked={mode === value}
                  disabled={busy}
                  onClick={() => setMode(value)}
                >
                  <SkillIcon skill={icon} size={22} />
                  {bi(vi, en)}
                </button>
              ))}
            </div>

            <div className="study-start">
              <button
                className="primary"
                disabled={busy || !ready || !saved || !!readError}
                onClick={() => start()}
              >
                <SkillIcon skill="check" size={20} />
                {remaining.length
                  ? bi(
                      `Bắt đầu luyện tập · còn ${remaining.length} từ →`,
                      `Start practice · ${remaining.length} left →`,
                    )
                  : bi('Ôn lại cụm này →', 'Review this group →')}
              </button>
              {nextGroup && (
                <button
                  disabled={busy || !ready || !saved}
                  onClick={() => start(nextGroup.id, false)}
                >
                  <SkillIcon skill="cap" size={20} />
                  {bi('Học cụm tiếp theo →', 'Study next group →')}
                </button>
              )}
            </div>
            <img
              className="study-books"
              src="/art/study-books.webp"
              width={386}
              height={130}
              alt=""
              draggable={false}
            />
          </>
        ) : (
          <p>
            {bi(
              'Chưa có từ trong bộ lọc này. Hãy chọn chủ đề hoặc trình độ khác.',
              'No words match these filters. Choose another topic or level.',
            )}
          </p>
        )}
      </section>
    </div>
  );
}
