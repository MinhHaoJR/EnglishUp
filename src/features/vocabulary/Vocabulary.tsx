import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useApp } from '../../app/store';
import SkillIcon, { type IconName } from '../../components/SkillIcon';

/** A sign for each group of topics in the directory. */
const sectionIcons: Record<string, IconName> = {
  everyday: 'streak',
  work: 'briefcase',
  specialist: 'cap',
  exam: 'achievements',
  writing: 'grammar',
};
import { vocabulary } from '../../data/content';
import { topicSectionFor, topicSections, type TopicSectionId } from '../../data/topicSections';
import { levelSchema, type Level, type Word } from '../../data/schema';
import { useT, useBi, topicVi } from '../../i18n';
import {
  PageTitle,
  Empty,
  Notice,
  useLive,
  useFiltered,
  LevelTopic,
} from '../../components/shared';
import { WordEditor } from '../../components/WordEditor';
import { SpeakButton } from '../../components/SpeakButton';
import { db, download } from '../../services/storage';
import { studyScope } from '../../services/vocabularyStudy';
import VocabularyPractice from './VocabularyPractice';
import { exportCSV } from '../../services/csv';
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
  const [picking, setPicking] = useState(false);
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
  const topicDirectory = (
    <section
      className="vocabulary-topics panel"
      aria-label={bi('Chọn chủ đề từ vựng', 'Choose a vocabulary topic')}
    >
      <div className="vocabulary-topic-heading">
        <h2>
          <SkillIcon skill="bookmark" size={22} />
          {bi('Chọn chủ đề', 'Choose a topic')}
        </h2>
        <button
          className="topic-all"
          aria-pressed={topic === 'all'}
          onClick={() => {
            filter(level, 'all');
            setPicking(false);
          }}
        >
          <SkillIcon skill="dashboard" size={18} />
          {t('allTopics')} · {all.filter((word) => level === 'all' || word.level === level).length}
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
              <SkillIcon skill={sectionIcons[entry.id] ?? 'vocabulary'} size={18} />
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
              onClick={() => {
                filter(level, group.topic);
                setPicking(false);
              }}
            >
              <span>{topicLabel(group.topic)}</span>
              <small>
                {count} {t('words')}
              </small>
              <span className="topic-tile-go" aria-hidden="true">
                <SkillIcon skill="chevron" size={16} />
              </span>
            </button>
          );
        })}
      </div>
      {activeTopics.length === 0 && (
        <p className="muted">{bi('Không tìm thấy chủ đề phù hợp.', 'No matching topics.')}</p>
      )}
    </section>
  );
  return (
    <>
      {/* Words are added only in the admin library; learners keep editing words they saved before. */}
      <PageTitle
        title={t('vocabulary')}
        description={bi(
          'Học thẻ từ, ôn tập ngắt quãng và luyện dịch',
          'Word cards, spaced review and translation',
        )}
      >
        <div className="vocab-hero" aria-hidden="true">
          <p className="vocab-slogan">
            <span>{bi('Học mỗi ngày', 'Learn every day,')}</span>
            <span>{bi('vững tương lai', 'build your future')}</span>
            <svg viewBox="0 0 60 30">
              <path className="plane" d="M58 2L30 13l9 3 3 9 5-8 11-15z" />
              <path className="trail" d="M30 16c-8 6-18 9-28 9" />
            </svg>
          </p>
          <img src="/art/vocab-books.webp" width={454} height={264} alt="" draggable={false} />
        </div>
      </PageTitle>
      {/* While a card is on screen, the totals step aside so the word has the page. */}
      {tab !== 'relations' && !(tab === 'practice' && practicing) && (
        <div className="stats">
          {(
            [
              [
                t('new'),
                all.length - reviews.filter((r) => all.some((w) => w.id === r.id)).length,
                'blue',
                'calendar',
              ],
              [t('learning'), reviews.filter((r) => r.interval < 21).length, 'green', 'cap'],
              [t('mastered'), reviews.filter((r) => r.interval >= 21).length, 'orange', 'clock'],
              [t('accuracy'), `${accuracy}%`, 'purple', 'goal'],
            ] as [string, number | string, string, IconName][]
          ).map(([label, n, tone, icon]) => (
            <div className="stat" key={label} data-tone={tone}>
              <span>
                <SkillIcon skill={icon} size={20} />
                {label}
              </span>
              <strong>{n}</strong>
              {tone === 'purple' ? (
                <svg className="stat-ring" viewBox="0 0 40 40" aria-hidden="true">
                  <circle cx="20" cy="20" r="15" />
                  <circle
                    cx="20"
                    cy="20"
                    r="15"
                    strokeDasharray={`${(accuracy / 100) * 94.2} 94.2`}
                  />
                </svg>
              ) : (
                <span className="stat-deco" aria-hidden="true">
                  <SkillIcon
                    skill={tone === 'blue' ? 'chart' : tone === 'green' ? 'cap' : 'achievements'}
                    size={44}
                  />
                </span>
              )}
            </div>
          ))}
        </div>
      )}
      {editing && tab !== 'relations' && (
        <WordEditor word={editing} onClose={() => setEditing(null)} />
      )}
      <div className="tabs">
        <button aria-pressed={tab === 'practice'} onClick={() => setTab('practice')}>
          <SkillIcon skill="bolt" size={18} />
          {t('practiceTab')}
        </button>
        <button aria-pressed={tab === 'library'} onClick={() => setTab('library')}>
          <SkillIcon skill="reading" size={18} />
          {t('library')} · {all.length}
        </button>
        <button aria-pressed={tab === 'translation'} onClick={() => setTab('translation')}>
          <SkillIcon skill="writing" size={18} />
          {bi('Luyện viết và dịch', 'Translation practice')}
        </button>
        <button aria-pressed={tab === 'relations'} onClick={() => setTab('relations')}>
          <SkillIcon skill="swap" size={18} />
          {bi('Đồng nghĩa & trái nghĩa', 'Synonyms & antonyms')}
        </button>
      </div>
      {/* One topic bar for every tab that lists words; the directory opens only when needed. */}
      {tab !== 'relations' && !(tab === 'practice' && practicing) && (
        <>
          <section className="panel topic-bar" aria-label={bi('Chủ đề đang học', 'Current topic')}>
            <img
              className="topic-bar-art"
              src="/art/vocab-book.webp"
              width={260}
              height={152}
              alt=""
              draggable={false}
            />
            <div className="topic-bar-name">
              <h2>
                <SkillIcon skill="star" size={22} />
                {topic === 'all' ? t('allTopics') : topicLabel(topic)}
              </h2>
              <small>
                {filtered.length} {t('words')}
              </small>
            </div>
            <label className="topic-bar-level">
              {t('level')}
              <select
                value={level}
                onChange={(event) => filter(event.target.value as Level | 'all', topic)}
              >
                <option value="all">{t('allLevels')}</option>
                {levelSchema.options.map((value) => (
                  <option key={value}>{value}</option>
                ))}
              </select>
            </label>
            {!(topic === 'all' && tab === 'practice') && (
              <button aria-expanded={picking} onClick={() => setPicking((open) => !open)}>
                {picking ? bi('Đóng danh sách', 'Close list') : bi('Đổi chủ đề', 'Change topic')}
              </button>
            )}
            <img
              className="topic-bar-art chart"
              src="/art/vocab-chart.webp"
              width={244}
              height={160}
              alt=""
              draggable={false}
            />
          </section>
          {/* Practice starts from the directory; the word list and translation start from their content. */}
          {((topic === 'all' && tab === 'practice') || picking) && topicDirectory}
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
                <SkillIcon skill="download" size={18} />
                {bi('Xuất CSV', 'Export CSV')}
              </button>
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
                      <LevelTopic level={w.level} topic={w.topic} />
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
