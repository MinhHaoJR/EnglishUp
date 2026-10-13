import { useEffect, useRef, useState } from 'react';
import type { Word } from '../../data/schema';
import { useApp } from '../../app/store';
import { useBi, useT, topicVi } from '../../i18n';
import { Notice, useLive } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
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
  const settings = useApp((state) => state.settings);
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

  if (card)
    return (
      <section className="panel flashcard vocabulary-study">
        {notices}
        <div className="study-card-meta">
          <span className="badge">
            {card.level} · {bi(topicVi[card.topic] ?? card.topic, card.topic)}
          </span>
          <span>
            {bi('Cụm', 'Group')} {activeGroup?.number} ·{' '}
            {(activeGroup?.words.findIndex((word) => word.id === card.id) ?? index) + 1} /{' '}
            {activeGroup?.words.length ?? queue.length}
          </span>
        </div>
        <progress
          value={activeGroup?.words.filter((word) => visited.has(word.id)).length ?? index}
          max={activeGroup?.words.length ?? queue.length}
          aria-label={t('progress')}
        />
        <div className="card-content">
          <h2 ref={heading} tabIndex={-1}>
            {mode === 'spell'
              ? bi('Nghe và viết từ', 'Listen and spell')
              : mode === 'type'
                ? card.meaning
                : card.word}
          </h2>
          {mode === 'type' ? (
            <p>{card.definition}</p>
          ) : (
            <>
              <p className="muted">
                {mode !== 'spell' && `${card.ipa ? `${card.ipa} · ` : ''}${card.pos}`}
              </p>
              <SpeakButton text={card.word} />
            </>
          )}
          <fieldset disabled={busy}>
            <legend className="sr-only">{bi('Trả lời thẻ từ', 'Answer the word card')}</legend>
            {mode === 'choice' && !revealed && (
              <div className="choice-grid">
                {options.map((option) => (
                  <button
                    key={option.id}
                    aria-pressed={answer === option.id}
                    className={answer === option.id ? 'primary' : ''}
                    onClick={() => setAnswer(option.id)}
                  >
                    {option.meaning}
                  </button>
                ))}
              </div>
            )}
            {(mode === 'type' || mode === 'spell') && !revealed && (
              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  if (answer.trim()) setRevealed(true);
                }}
              >
                <label>
                  {t('answer')}
                  <input
                    autoComplete="off"
                    value={answer}
                    onChange={(event) => setAnswer(event.target.value)}
                  />
                </label>
                <button className="primary mt-4" disabled={!answer.trim()}>
                  {t('check')}
                </button>
              </form>
            )}
            {revealed ? (
              <>
                <div className="answer-box">
                  {mode !== 'flashcards' && (
                    <strong>{matched ? t('correct') : bi('Đáp án đúng', 'Correct answer')}</strong>
                  )}
                  <h3>
                    {card.word} — {card.meaning}
                  </h3>
                  <p>{card.definition}</p>
                  {card.examples.map((example) => (
                    <p key={example}>
                      <em>{example}</em>
                    </p>
                  ))}
                </div>
                <p className="muted">
                  {bi('Bạn nhớ từ này tốt đến đâu?', 'How well did you remember?')}
                </p>
                <div className="actions justify-center">
                  {(['again', 'hard', 'good', 'easy'] as const).map((rating) => (
                    <button
                      key={rating}
                      disabled={mode !== 'flashcards' && !matched && rating !== 'again'}
                      onClick={() => advance(rating)}
                    >
                      {t(rating)}
                    </button>
                  ))}
                </div>
              </>
            ) : mode === 'flashcards' ? (
              <button className="primary mt-6" onClick={() => setRevealed(true)}>
                {t('reveal')}
              </button>
            ) : mode === 'choice' ? (
              <button className="primary mt-5" disabled={!answer} onClick={() => setRevealed(true)}>
                {t('check')}
              </button>
            ) : null}
          </fieldset>
        </div>
        <div className="study-session-actions">
          <button disabled={busy} className="study-skip" onClick={() => advance()}>
            {bi('Bỏ qua / Tiếp tục →', 'Skip word →')}
          </button>
          <button
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
        <p className="muted">
          {bi(
            'Bỏ qua không chấm điểm. Lần học tiếp sẽ bắt đầu từ từ chưa đi qua trong cụm.',
            'Skipping does not score the word. Continue later from the next unvisited word in this group.',
          )}
        </p>
      </section>
    );

  return (
    <div className="vocabulary-study">
      {notices}
      <section className="panel study-chooser">
        <div className="study-heading">
          <span className="study-mark" aria-hidden="true">
            Aa
          </span>
          <div>
            <h2 ref={chooser} tabIndex={-1}>
              {finished ? t('result') : bi('Chọn cụm từ để học', 'Choose a word group')}
            </h2>
            <p className="muted">
              {bi(
                'Mỗi cụm tối đa 20 từ · Không giới hạn học mỗi ngày',
                'Up to 20 words per group · No daily study limit',
              )}
            </p>
          </div>
        </div>
        {finished && (
          <Notice>
            {bi(
              `Lượt này: ${rated} từ đã đánh giá, ${skipped} từ bỏ qua. Bạn có thể học tiếp cụm khác ngay.`,
              `This session: ${rated} rated, ${skipped} skipped. You can start another group now.`,
            )}
          </Notice>
        )}
        {selected ? (
          <>
            <div className="form-grid">
              <label>
                {bi('Cụm từ vựng', 'Word group')}
                <select
                  disabled={busy || !ready || !saved}
                  value={selected.id}
                  onChange={(event) => {
                    const id = event.target.value;
                    void run(async () => {
                      await selectStudyGroup(scope, words, id);
                      setFinished(false);
                    });
                  }}
                >
                  {groups.map((group) => (
                    <option key={group.id} value={group.id}>
                      {bi('Cụm', 'Group')} {group.number} · {(group.number - 1) * 20 + 1}–
                      {(group.number - 1) * 20 + group.words.length} ·{' '}
                      {group.words.filter((word) => visited.has(word.id)).length}/
                      {group.words.length} {bi('đã đi qua', 'visited')}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {bi('Cách luyện tập', 'Practice mode')}
                <select
                  value={mode}
                  disabled={busy}
                  onChange={(event) => setMode(event.target.value as Mode)}
                >
                  <option value="flashcards">{bi('Thẻ ghi nhớ', 'Flashcards')}</option>
                  <option value="choice">{bi('Chọn nghĩa đúng', 'Multiple choice')}</option>
                  <option value="type">{bi('Gõ từ tiếng Anh', 'Type the word')}</option>
                  <option value="spell">{bi('Nghe và viết từ', 'Listen and spell')}</option>
                </select>
              </label>
            </div>
            <p className="study-summary" role="status">
              {bi(
                `Cụm ${selected.number}: ${selected.words.length - remaining.length}/${selected.words.length} từ đã đi qua · Còn ${remaining.length} từ`,
                `Group ${selected.number}: ${selected.words.length - remaining.length}/${selected.words.length} visited · ${remaining.length} remaining`,
              )}
            </p>
            <details className="study-preview">
              <summary>
                {bi(
                  `Xem ${selected.words.length} từ trong cụm`,
                  `Preview ${selected.words.length} words`,
                )}
              </summary>
              <ol>
                {selected.words.map((word) => (
                  <li key={word.id}>
                    <span lang="en">{word.word}</span>
                    {visited.has(word.id) && <small>{bi('Đã đi qua', 'Visited')}</small>}
                  </li>
                ))}
              </ol>
            </details>
            <div className="actions mt-5">
              <button
                className="primary"
                disabled={busy || !ready || !saved || !!readError}
                onClick={() => start()}
              >
                {remaining.length
                  ? `${bi('Bắt đầu luyện tập / Tiếp tục', 'Start practice / Continue')} →`
                  : bi('Ôn lại cụm này →', 'Review this group →')}
              </button>
              {nextGroup && (
                <button
                  disabled={busy || !ready || !saved}
                  onClick={() => start(nextGroup.id, false)}
                >
                  {bi('Học cụm tiếp theo →', 'Study next group →')}
                </button>
              )}
            </div>
            <p className="muted">
              {bi(
                'Tiến độ tự lưu sau mỗi lần đánh giá hoặc bỏ qua. Chọn “Ôn lại cụm này” khi muốn học lại cụm đã hoàn tất.',
                'Progress saves after every rating or skip. Choose “Review this group” to repeat a completed group.',
              )}
            </p>
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
      <section className="panel">
        <h2>{t('upcoming')}</h2>
        <div className="upcoming-grid">
          {Array.from({ length: 7 }, (_, index) => {
            const from = new Date();
            from.setDate(from.getDate() + index + 1);
            from.setHours(0, 0, 0, 0);
            const to = new Date(from);
            to.setDate(to.getDate() + 1);
            return (
              <div key={index}>
                <span className="muted">
                  {from.toLocaleDateString(settings.language, { weekday: 'short', day: 'numeric' })}
                </span>
                <strong>
                  {
                    (saved?.reviews ?? []).filter(
                      (review) => review.due >= +from && review.due < +to,
                    ).length
                  }
                </strong>
              </div>
            );
          })}
        </div>
        <p className="muted">
          {bi(
            'Lịch ôn là gợi ý. Bạn vẫn có thể chọn bất kỳ cụm nào để học.',
            'The review schedule is a suggestion. You can study any group at any time.',
          )}
        </p>
      </section>
    </div>
  );
}
