import { useState } from 'react';
import { useApp } from '../../app/store';
import { vocabulary } from '../../data/content';
import type { Word } from '../../data/schema';
import { useT, useBi, topicVi } from '../../i18n';
import { PageTitle, Filters, Empty, Notice, useLive, useFiltered } from '../../components/shared';
import { WordEditor } from '../../components/WordEditor';
import { SpeakButton } from '../../components/SpeakButton';
import { db, download } from '../../services/storage';
import { dueQueue, schedule, type Rating } from '../../services/srs';
import { importCSV, exportCSV } from '../../services/csv';
import TranslationPractice from './TranslationPractice';
import { groupWords, searchWords, paginateWords } from '../../services/vocabulary';
type Mode = 'flashcards' | 'choice' | 'type' | 'spell';
export default function Vocabulary() {
  const t = useT();
  const bi = useBi();
  const { settings, level, topic, filter } = useApp();
  const { value: custom = [], error } = useLive(() => db.words.toArray());
  const { value: reviews = [] } = useLive(() => db.reviews.toArray());
  const all = [...vocabulary, ...custom];
  const filtered = useFiltered(all);
  const [tab, setTab] = useState<'practice' | 'library' | 'translation'>('practice');
  const [mode, setMode] = useState<Mode>('flashcards');
  const [queue, setQueue] = useState<Word[]>([]);
  const [index, setIndex] = useState(0);
  const [started, setStarted] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [answer, setAnswer] = useState('');
  const [editing, setEditing] = useState<Partial<Word> | null>(null);
  const [search, setSearch] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [finished, setFinished] = useState(false);
  const [pagination, setPagination] = useState({ key: '', page: 0 });
  const topicGroups = groupWords(all);
  const searchResults = searchWords(filtered, search);
  const pageKey = JSON.stringify([level, topic, search]);
  // Reset the stored cursor too, so returning to a previous search cannot restore a stale page.
  if (pagination.key !== pageKey) setPagination({ key: pageKey, page: 0 });
  const pageData = paginateWords(searchResults, pagination.key === pageKey ? pagination.page : 0);
  const libraryGroups = groupWords(pageData.words);
  const changePage = (page: number) => setPagination({ key: pageKey, page });
  const topicLabel = (name: string) => bi(topicVi[name] ?? name, name);
  const due = dueQueue(filtered, reviews, settings.newCards);
  const card = queue[index];
  const total = reviews.reduce((n, r) => n + r.total, 0);
  const accuracy = total
    ? Math.round((reviews.reduce((n, r) => n + r.correct, 0) / total) * 100)
    : 0;
  const matched =
    card &&
    (mode === 'choice'
      ? answer === card.id
      : answer.trim().toLowerCase() === card.word.toLowerCase());
  const options = card
    ? [
        card,
        ...all
          .filter((w) => w.id !== card.id && w.meaning !== card.meaning)
          .slice(index % 20, (index % 20) + 3),
      ].sort((a, b) => a.meaning.localeCompare(b.meaning))
    : [];
  async function rate(rating: Rating) {
    if (!card || busy) return;
    setBusy(true);
    try {
      const now = Date.now();
      await db.transaction('rw', db.reviews, db.attempts, async () => {
        const prior = await db.reviews.get(card.id);
        await db.reviews.put(schedule(card.id, rating, prior, now));
        await db.attempts.add({
          id: crypto.randomUUID(),
          skill: 'vocabulary',
          score: rating === 'again' ? 0 : rating === 'hard' ? 60 : rating === 'good' ? 85 : 100,
          duration: Math.max(1, Math.round((now - started) / 1000)),
          timestamp: now,
          label: card.word,
        });
      });
      setIndex(index + 1);
      setRevealed(false);
      setAnswer('');
      setStarted(Date.now());
      if (index + 1 === queue.length) setFinished(true);
    } catch {
      setMessage(t('error'));
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <PageTitle
        eyebrow={bi('NHỮNG TỪ BẠN SẼ NHỚ', 'WORDS THAT STAY WITH YOU')}
        title={t('vocabulary')}
        description={bi(
          'Học từ trong ngữ cảnh. Ôn lại đúng lúc.',
          'Learn in context. Review at the right time.',
        )}
      >
        <button className="primary" onClick={() => setEditing({})}>
          ＋ {t('add')}
        </button>
      </PageTitle>
      <div className="stats">
        {[
          [t('new'), all.length - reviews.filter((r) => all.some((w) => w.id === r.id)).length],
          [t('learning'), reviews.filter((r) => r.interval < 21).length],
          [t('mastered'), reviews.filter((r) => r.interval >= 21).length],
          [t('accuracy'), `${accuracy}%`],
        ].map(([label, n]) => (
          <div className="stat" key={label}>
            <span>{label}</span>
            <strong>{n}</strong>
          </div>
        ))}
      </div>
      {editing && <WordEditor word={editing} onClose={() => setEditing(null)} />}
      <div className="tabs">
        <button aria-pressed={tab === 'practice'} onClick={() => setTab('practice')}>
          {t('practiceTab')}
        </button>
        <button aria-pressed={tab === 'library'} onClick={() => setTab('library')}>
          {t('library')} · {all.length}
        </button>
        <button aria-pressed={tab === 'translation'} onClick={() => setTab('translation')}>
          {bi('Luyện viết và dịch', 'Translation practice')}
        </button>
      </div>
      {(!card || tab !== 'practice') && (
        <>
          <Filters availableTopics={topicGroups.map((group) => group.topic)} />
          <section
            className="vocabulary-topics panel space-y-4"
            aria-label={bi('Chọn chủ đề từ vựng', 'Choose a vocabulary topic')}
          >
            <div className="actions">
              <h2>{bi('Học theo chủ đề', 'Learn by topic')}</h2>
              <button aria-pressed={topic === 'all'} onClick={() => filter(level, 'all')}>
                {t('allTopics')} ·{' '}
                {all.filter((word) => level === 'all' || word.level === level).length}
              </button>
            </div>
            {[false, true].map((it) => (
              <div key={String(it)}>
                <h3>
                  {it
                    ? bi('Tiếng Anh chuyên ngành IT', 'English for IT')
                    : bi('Đời sống và công việc', 'Everyday life and work')}
                </h3>
                <div className="topic-choices actions mt-2">
                  {topicGroups
                    .filter((group) => group.topic.startsWith('IT:') === it)
                    .map((group) => (
                      <button
                        key={group.topic}
                        aria-pressed={topic === group.topic}
                        className={topic === group.topic ? 'primary' : ''}
                        onClick={() => filter(level, group.topic)}
                      >
                        {topicLabel(group.topic)} ·{' '}
                        {
                          group.words.filter((word) => level === 'all' || word.level === level)
                            .length
                        }
                      </button>
                    ))}
                </div>
              </div>
            ))}
            <p className="muted">
              {bi(
                'Số từ theo trình độ đang chọn. Chọn chủ đề để xem từ và luyện tập.',
                'Counts reflect the selected level. Choose a topic to browse and practice.',
              )}
            </p>
          </section>
        </>
      )}
      {error && <Notice error>{error}</Notice>}
      {message && <Notice>{message}</Notice>}
      {tab === 'translation' ? (
        <TranslationPractice words={filtered} />
      ) : tab === 'library' ? (
        <>
          <div className="panel space-y-4">
            <label>
              {t('search')}
              <input type="search" value={search} onChange={(e) => setSearch(e.target.value)} />
            </label>
            <div className="actions">
              <button
                onClick={() =>
                  download('englishup-words.csv', exportCSV(filtered), 'text/csv;charset=utf-8')
                }
              >
                ↓ {bi('Xuất CSV', 'Export CSV')}
              </button>
              <label className="button">
                ↑ {bi('Nhập CSV', 'Import CSV')}
                <input
                  className="sr-only"
                  type="file"
                  accept=".csv,text/csv"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file)
                      void (async () => {
                        try {
                          const rows = importCSV(await file.text());
                          await db.words.bulkAdd(rows);
                          setMessage(`${rows.length} ${t('saved')}`);
                        } catch {
                          setMessage(
                            bi(
                              'CSV không hợp lệ. Xem định dạng trong docs/CONTENT.md.',
                              'Invalid CSV. See docs/CONTENT.md for the format.',
                            ),
                          );
                        }
                      })();
                    e.target.value = '';
                  }}
                />
              </label>
            </div>
          </div>
          {searchResults.length > 0 && (
            <nav
              className="panel actions"
              aria-label={bi('Phân trang từ vựng', 'Vocabulary pages')}
            >
              <button disabled={pageData.page === 0} onClick={() => changePage(pageData.page - 1)}>
                {bi('Trang trước', 'Previous page')}
              </button>
              <label>
                {bi('Trang', 'Page')}
                <select
                  value={pageData.page}
                  onChange={(event) => changePage(Number(event.target.value))}
                >
                  {Array.from({ length: pageData.pageCount }, (_, page) => (
                    <option key={page} value={page}>
                      {page + 1} / {pageData.pageCount}
                    </option>
                  ))}
                </select>
              </label>
              <button
                disabled={pageData.page + 1 === pageData.pageCount}
                onClick={() => changePage(pageData.page + 1)}
              >
                {bi('Trang sau', 'Next page')}
              </button>
              <span role="status">
                {bi(
                  `Trang ${pageData.page + 1}/${pageData.pageCount} · ${searchResults.length} từ phù hợp`,
                  `Page ${pageData.page + 1}/${pageData.pageCount} · ${searchResults.length} matching words`,
                )}
              </span>
            </nav>
          )}
          {libraryGroups.map((group) => (
            <section key={group.topic} aria-label={topicLabel(group.topic)} className="space-y-4">
              <h2>
                {topicLabel(group.topic)} ·{' '}
                {searchResults.filter((word) => word.topic === group.topic).length} {t('words')}
              </h2>
              <div className="lesson-grid">
                {group.words.map((w) => (
                  <article className="panel lesson-card" key={w.id}>
                    <div className="flex justify-between w-full">
                      <span className="badge">
                        {w.level} · {topicLabel(w.topic)}
                      </span>
                      {w.custom && <span className="badge">{t('custom')}</span>}
                    </div>
                    <h2>
                      {w.word}{' '}
                      <small className="muted">
                        {w.ipa ? `${w.ipa} · ` : ''}
                        {w.pos}
                      </small>
                    </h2>
                    <strong>{w.meaning}</strong>
                    <p className="muted">
                      {w.definition}
                      <br />
                      <em>{w.examples[0]}</em>
                    </p>
                    <div className="actions">
                      <SpeakButton text={w.word} />
                      {w.custom && (
                        <>
                          <button onClick={() => setEditing(w)}>{t('edit')}</button>
                          <button
                            className="danger"
                            onClick={() => {
                              if (window.confirm(bi(`Xóa từ “${w.word}”?`, `Delete “${w.word}”?`)))
                                void db
                                  .transaction('rw', db.words, db.reviews, async () => {
                                    await db.words.delete(w.id);
                                    await db.reviews.delete(w.id);
                                  })
                                  .catch(() => setMessage(t('error')));
                            }}
                          >
                            {t('delete')}
                          </button>
                        </>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ))}
          {!libraryGroups.length && (
            <>
              <Empty />
              {search && (
                <button onClick={() => setSearch('')}>{bi('Xóa tìm kiếm', 'Clear search')}</button>
              )}
            </>
          )}
        </>
      ) : card ? (
        <section className="panel flashcard">
          <div className="flex justify-between">
            <span className="badge">
              {card.level} · {topicLabel(card.topic)}
            </span>
            <span className="muted">
              {index + 1} / {queue.length}
            </span>
          </div>
          <progress value={index} max={queue.length} aria-label={t('progress')} />
          <div className="card-content">
            {mode === 'spell' ? (
              <SpeakButton text={card.word} />
            ) : mode === 'type' ? (
              <>
                <p className="eyebrow">{bi('TỪ NÀO PHÙ HỢP?', 'WHICH WORD FITS?')}</p>
                <h2>{card.meaning}</h2>
                <p>{card.definition}</p>
              </>
            ) : (
              <>
                <h2>{card.word}</h2>
                <p className="muted">
                  {card.ipa ? `${card.ipa} · ` : ''}
                  {card.pos}
                </p>
                <SpeakButton text={card.word} />
              </>
            )}
            {mode === 'choice' && !revealed && (
              <div className="choice-grid">
                {options.map((o) => (
                  <button
                    key={o.id}
                    aria-pressed={answer === o.id}
                    className={answer === o.id ? 'primary' : ''}
                    onClick={() => setAnswer(o.id)}
                  >
                    {o.meaning}
                  </button>
                ))}
              </div>
            )}
            {(mode === 'type' || mode === 'spell') && !revealed && (
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  setRevealed(true);
                }}
              >
                <label>
                  {t('answer')}
                  <input
                    autoComplete="off"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
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
                  {card.examples.map((s) => (
                    <p key={s}>
                      <em>{s}</em>
                    </p>
                  ))}
                </div>
                <p className="muted">
                  {bi('Bạn nhớ từ này tốt đến đâu?', 'How well did you remember?')}
                </p>
                <div className="actions justify-center">
                  {(['again', 'hard', 'good', 'easy'] as Rating[]).map((r) => (
                    <button
                      disabled={busy || (mode !== 'flashcards' && !matched && r !== 'again')}
                      key={r}
                      onClick={() => void rate(r)}
                    >
                      {t(r)}
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
          </div>
          <button
            onClick={() => {
              setQueue([]);
              setFinished(false);
            }}
          >
            {bi('Kết thúc sớm (giữ kết quả đã lưu)', 'End early (keep saved reviews)')}
          </button>
        </section>
      ) : (
        <>
          <section className="panel practice-intro">
            <span className="big-glyph" aria-hidden="true">
              Aa
            </span>
            <div>
              <h2>
                {finished
                  ? t('result')
                  : bi(
                      'Một chút mỗi ngày, nhớ lâu hơn',
                      'A little every day, remembered for longer',
                    )}
              </h2>
              <p className="muted">
                {due.length}{' '}
                {bi(
                  'thẻ sẵn sàng • tối đa 10 thẻ mỗi buổi',
                  'cards ready • up to 10 cards per session',
                )}
              </p>
              <label>
                {bi('Cách luyện tập', 'Practice mode')}
                <select value={mode} onChange={(e) => setMode(e.target.value as Mode)}>
                  <option value="flashcards">{bi('Thẻ ghi nhớ', 'Flashcards')}</option>
                  <option value="choice">{bi('Chọn nghĩa đúng', 'Multiple choice')}</option>
                  <option value="type">{bi('Gõ từ tiếng Anh', 'Type the word')}</option>
                  <option value="spell">{bi('Nghe và viết từ', 'Listen and spell')}</option>
                </select>
              </label>
              <button
                className="primary mt-5"
                disabled={!due.length}
                onClick={() => {
                  setQueue(due.slice(0, 10));
                  setIndex(0);
                  setStarted(Date.now());
                  setAnswer('');
                  setRevealed(false);
                  setFinished(false);
                }}
              >
                {t('start')} →
              </button>
              {!due.length && (
                <p className="muted">
                  {bi(
                    'Đã hết thẻ đến hạn hoặc đạt giới hạn từ mới hôm nay.',
                    'No cards due, or today’s new-card limit is reached.',
                  )}
                </p>
              )}
            </div>
          </section>
          <section className="panel">
            <h2>{t('upcoming')}</h2>
            <div className="upcoming-grid">
              {Array.from({ length: 7 }, (_, i) => {
                const a = new Date();
                a.setDate(a.getDate() + i + 1);
                a.setHours(0, 0, 0, 0);
                const b = new Date(a);
                b.setDate(b.getDate() + 1);
                return (
                  <div key={i}>
                    <span className="muted">
                      {a.toLocaleDateString(settings.language, {
                        weekday: 'short',
                        day: 'numeric',
                      })}
                    </span>
                    <strong>{reviews.filter((r) => r.due >= +a && r.due < +b).length}</strong>
                  </div>
                );
              })}
            </div>
          </section>
        </>
      )}
    </>
  );
}
