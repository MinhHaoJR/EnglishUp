import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useApp } from '../../app/store';
import { vocabulary } from '../../data/content';
import { topicSectionFor, topicSections, type TopicSectionId } from '../../data/topicSections';
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
import '../../styles/vocabulary-topics.css';
export default function Vocabulary() {
  const t = useT();
  const bi = useBi();
  const { level, topic, filter } = useApp();
  const { value: customWords, error } = useLive(() => db.words.toArray());
  const custom = customWords ?? [];
  const [practicing, setPracticing] = useState(false);
  const [section, setSection] = useState<TopicSectionId>(
    topic === 'all' ? 'everyday' : topicSectionFor(topic),
  );
  const [topicSearch, setTopicSearch] = useState('');
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
  const topicLabel = (name: string) => bi(topicVi[name] ?? name, name);
  const topicGroups = groupWords(all);
  const knownTopics = new Set<string>(topicSections.flatMap((entry) => [...entry.topics]));
  const customTopics = topicGroups
    .map((group) => group.topic)
    .filter((name) => !knownTopics.has(name));
  const topicOptionGroups = [
    ...topicSections.map((entry) => ({ label: bi(entry.vi, entry.en), topics: entry.topics })),
    ...(customTopics.length ? [{ label: bi('Tự thêm', 'Custom'), topics: customTopics }] : []),
  ];
  const normalizeTopic = (value: string) =>
    value.normalize('NFD').replace(/\p{M}/gu, '').replace(/[đĐ]/g, 'd').toLowerCase();
  const topicRank = new Map<string, number>(
    topicSections.flatMap((entry) => [...entry.topics]).map((name, index) => [name, index]),
  );
  const activeTopics = topicGroups
    .filter((group) =>
      topicSearch.trim()
        ? normalizeTopic(topicLabel(group.topic)).includes(normalizeTopic(topicSearch.trim())) ||
          normalizeTopic(group.topic).includes(normalizeTopic(topicSearch.trim()))
        : section === 'custom'
          ? customTopics.includes(group.topic)
          : topicSectionFor(group.topic) === section,
    )
    .sort(
      (a, b) =>
        (topicRank.get(a.topic) ?? Number.MAX_SAFE_INTEGER) -
          (topicRank.get(b.topic) ?? Number.MAX_SAFE_INTEGER) ||
        topicLabel(a.topic).localeCompare(topicLabel(b.topic)),
    );
  useEffect(() => {
    if (topic !== 'all') {
      setSection(topicSectionFor(topic));
      setTopicSearch('');
    }
  }, [topic]);
  const searchResults = searchWords(filtered, search);
  const pageKey = JSON.stringify([level, topic, search]);
  // Reset the stored cursor too, so returning to a previous search cannot restore a stale page.
  if (pagination.key !== pageKey) setPagination({ key: pageKey, page: 0 });
  const pageData = paginateWords(searchResults, pagination.key === pageKey ? pagination.page : 0);
  const libraryGroups = groupWords(pageData.words);
  const changePage = (page: number) => setPagination({ key: pageKey, page });
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
          <Filters
            availableTopics={topicGroups.map((group) => group.topic)}
            topicOptionGroups={topicOptionGroups}
          />
          <section
            className="vocabulary-topics panel"
            aria-label={bi('Chọn chủ đề từ vựng', 'Choose a vocabulary topic')}
          >
            <div className="vocabulary-topic-heading">
              <div>
                <h2>{bi('Chọn chủ đề', 'Choose a topic')}</h2>
                <p className="muted">
                  {bi(
                    'Lọc theo nhóm hoặc tìm nhanh tên chủ đề.',
                    'Browse a group or search by topic name.',
                  )}
                </p>
              </div>
              <button
                className="topic-all"
                aria-pressed={topic === 'all'}
                onClick={() => filter(level, 'all')}
              >
                {t('allTopics')} ·{' '}
                {all.filter((word) => level === 'all' || word.level === level).length}
              </button>
            </div>
            <div className="topic-toolbar">
              <nav className="topic-sections" aria-label={bi('Nhóm chủ đề', 'Topic groups')}>
                {topicSections.map((entry) => (
                  <button
                    key={entry.id}
                    aria-pressed={section === entry.id && !topicSearch}
                    onClick={() => {
                      setSection(entry.id);
                      setTopicSearch('');
                      filter(level, 'all');
                    }}
                  >
                    {bi(entry.vi, entry.en)}
                  </button>
                ))}
                {customTopics.length > 0 && (
                  <button
                    aria-pressed={section === 'custom' && !topicSearch}
                    onClick={() => {
                      setSection('custom');
                      setTopicSearch('');
                      filter(level, 'all');
                    }}
                  >
                    {bi('Tự thêm', 'Custom')}
                  </button>
                )}
              </nav>
              <label className="topic-search">
                {bi('Tìm chủ đề', 'Find a topic')}
                <input
                  type="search"
                  value={topicSearch}
                  onChange={(event) => setTopicSearch(event.target.value)}
                  placeholder={bi('Ví dụ: marketing', 'e.g. marketing')}
                />
              </label>
            </div>
            {section === 'exam' && !topicSearch && (
              <p className="topic-guidance muted">
                {bi(
                  'Từ C1–C2 để luyện đọc, viết và lập luận học thuật. Nhãn cấp độ mang tính gợi ý.',
                  'C1–C2 words for academic reading, writing and argument. Levels are editorial guidance.',
                )}
              </p>
            )}
            <div className="topic-grid">
              {activeTopics.map((group) => {
                const count = group.words.filter(
                  (word) => level === 'all' || word.level === level,
                ).length;
                return (
                  <button
                    key={group.topic}
                    className="topic-tile"
                    aria-pressed={topic === group.topic}
                    disabled={count === 0}
                    onClick={() => filter(level, group.topic)}
                  >
                    <span>{topicLabel(group.topic)}</span>
                    <small>
                      {count} {t('words')}
                    </small>
                  </button>
                );
              })}
            </div>
            {activeTopics.length === 0 && (
              <p className="muted">{bi('Không tìm thấy chủ đề phù hợp.', 'No matching topics.')}</p>
            )}
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
