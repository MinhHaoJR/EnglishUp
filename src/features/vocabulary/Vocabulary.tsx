import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useApp } from '../../app/store';
import { vocabulary } from '../../data/content';
import type { Word } from '../../data/schema';
import { useT, useBi, topicVi } from '../../i18n';
import { PageTitle, Filters, Empty, Notice, useLive, useFiltered } from '../../components/shared';
import { WordEditor } from '../../components/WordEditor';
import { SpeakButton } from '../../components/SpeakButton';
import { db, download } from '../../services/storage';
import { studyScope } from '../../services/vocabularyStudy';
import VocabularyPractice from './VocabularyPractice';
import { importCSV, exportCSV } from '../../services/csv';
import TranslationPractice from './TranslationPractice';
import WordRelations from './WordRelations';
import { groupWords, searchWords, paginateWords } from '../../services/vocabulary';
export default function Vocabulary() {
  const t = useT();
  const bi = useBi();
  const { level, topic, filter } = useApp();
  const { value: customWords, error } = useLive(() => db.words.toArray());
  const custom = customWords ?? [];
  const [practicing, setPracticing] = useState(false);
  const { value: reviews = [] } = useLive(() => db.reviews.toArray());
  const all = [...vocabulary, ...custom];
  const filtered = useFiltered(all);
  const [searchParams, setSearchParams] = useSearchParams();
  const requestedTab = searchParams.get('tab');
  const tab =
    requestedTab === 'library' || requestedTab === 'translation' || requestedTab === 'relations'
      ? requestedTab
      : 'practice';
  function setTab(next: 'practice' | 'library' | 'translation' | 'relations') {
    setSearchParams((previous) => {
      const params = new URLSearchParams(previous);
      if (next === 'practice') params.delete('tab');
      else params.set('tab', next);
      return params;
    });
  }
  const [editing, setEditing] = useState<Partial<Word> | null>(null);
  const [search, setSearch] = useState('');
  const [message, setMessage] = useState('');
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
  const total = reviews.reduce((n, r) => n + r.total, 0);
  const accuracy = total
    ? Math.round((reviews.reduce((n, r) => n + r.correct, 0) / total) * 100)
    : 0;
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
        {tab !== 'relations' && (
          <button className="primary" onClick={() => setEditing({})}>
            ＋ {t('add')}
          </button>
        )}
      </PageTitle>
      {tab !== 'relations' && (
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
      )}
      {editing && tab !== 'relations' && (
        <WordEditor word={editing} onClose={() => setEditing(null)} />
      )}
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
        <button aria-pressed={tab === 'relations'} onClick={() => setTab('relations')}>
          {bi('Đồng nghĩa & trái nghĩa', 'Synonyms & antonyms')}
        </button>
      </div>
      {tab !== 'relations' && (!practicing || tab !== 'practice') && (
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
      {tab === 'relations' ? (
        <WordRelations />
      ) : tab === 'translation' ? (
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
      ) : (
        <VocabularyPractice
          key={studyScope(level, topic)}
          scope={studyScope(level, topic)}
          words={filtered}
          all={all}
          ready={customWords !== undefined}
          onActiveChange={setPracticing}
        />
      )}
    </>
  );
}
