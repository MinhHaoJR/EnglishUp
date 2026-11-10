import { useEffect, useMemo, useState } from 'react';
import { useBi, topicVi } from '../../i18n';
import { Notice } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import {
  levelSchema,
  quizCategories,
  structureGroups,
  type QuizCategory,
  type StructureGroup,
} from '../../data/schema';
import { groupLabels } from '../grammar/Grammar';
import ContentForm, { blankItem } from './ContentForm';
import { topicSections } from '../../data/topicSections';
import { STUDY_GROUP_SIZE } from '../../services/vocabularyStudy';
import { ApiError } from '../../services/auth';
import {
  deleteContent,
  fetchContentRows,
  hideContent,
  loadContent,
  parseRow,
  saveContent,
  type ContentKind,
  type ContentRow,
} from '../../services/content';

type Item = { id: string } & Record<string, unknown>;
type Status = 'live' | 'hidden' | 'invalid';
type Entry = { id: string; item: Item | null; status: Status; row: ContentRow };

/** Each kind with its icon and the skill line that tints its tab. */
const kinds: { id: ContentKind; icon: IconName; skill: string; vi: string; en: string }[] = [
  { id: 'word', icon: 'vocabulary', skill: 'vocabulary', vi: 'Từ vựng', en: 'Vocabulary' },
  {
    id: 'structure',
    icon: 'grammar',
    skill: 'grammar',
    vi: 'Cấu trúc câu',
    en: 'Sentence patterns',
  },
  { id: 'reading', icon: 'reading', skill: 'reading', vi: 'Bài đọc', en: 'Readings' },
  { id: 'listening', icon: 'listening', skill: 'listening', vi: 'Bài nghe', en: 'Listening' },
  { id: 'dictation', icon: 'keyboard', skill: 'listening', vi: 'Chép chính tả', en: 'Dictation' },
  { id: 'speaking', icon: 'speaking', skill: 'speaking', vi: 'Luyện nói', en: 'Speaking' },
  { id: 'writing', icon: 'writing', skill: 'writing', vi: 'Luyện viết', en: 'Writing' },
  { id: 'translation', icon: 'choice', skill: 'vocabulary', vi: 'Câu dịch', en: 'Translations' },
  {
    id: 'relation',
    icon: 'cards',
    skill: 'vocabulary',
    vi: 'Đồng nghĩa – trái nghĩa',
    en: 'Synonyms & antonyms',
  },
  { id: 'quiz', icon: 'choice', skill: 'grammar', vi: 'Câu hỏi ngữ pháp', en: 'Grammar questions' },
  { id: 'roadmap', icon: 'roadmap', skill: 'reading', vi: 'Lộ trình học', en: 'Learning paths' },
];

/** One line that names an item in the list, whatever its kind. */
function label(kind: ContentKind, item: Item) {
  if (kind === 'word' || kind === 'relation')
    return `${String(item.word)} — ${String(item.meaning)}`;
  if (kind === 'translation') return String((item.en as string[] | undefined)?.[0]);
  if (kind === 'structure') return String(item.formula);
  if (kind === 'quiz') return `${String(item.sentence)} → ${String(item.answer)}`;
  if (kind === 'roadmap') return String((item.title as { vi?: string } | undefined)?.vi);
  if (kind === 'dictation') return String(item.text);
  return String(item.title);
}

/** A fresh id: s### for sentence patterns (their schema requires it), a dated one for the rest. */
function newId(kind: ContentKind, taken: Set<string>) {
  if (kind === 'structure') {
    for (let n = 101; n < 1000; n++) if (!taken.has(`s${n}`)) return `s${n}`;
  }
  return `a-${kind}-${Date.now().toString(36)}`;
}

/** The library's items of one kind, in the app's order, with whether learners see each one. */
function entries(kind: ContentKind, rows: ContentRow[]): Entry[] {
  return rows
    .filter((row) => row.kind === kind)
    .map((row) => {
      const item = parseRow(row) as Item | null;
      return { id: row.id, item, row, status: row.hidden ? 'hidden' : item ? 'live' : 'invalid' };
    });
}

type Group = {
  key: string;
  /** Vietnamese and English names of the group. */
  name: [string, string];
  total: number;
  /**
   * The visible items. Words come in the same 20-word clusters learners study (numbered from 1);
   * other kinds are one unnumbered block, as their pages show them.
   */
  clusters: { number: number; words: Entry[] }[];
  /** Hidden or invalid items: learners do not see them, so they are in no cluster. */
  other: Entry[];
};
const catalogOrder: string[] = topicSections.flatMap((section) => [...section.topics]);
const levels: string[] = [...levelSchema.options];

/** How each kind is grouped in the list: by topic, by grammar group (patterns) or by level (synonyms). */
function grouping(kind: ContentKind) {
  if (kind === 'structure')
    return {
      key: (item: Item) => String(item.group),
      order: [...structureGroups] as string[],
      name: (key: string): [string, string] => groupLabels[key as StructureGroup] ?? [key, key],
    };
  if (kind === 'quiz')
    return {
      key: (item: Item) => String(item.category),
      order: Object.keys(quizCategories),
      name: (key: string): [string, string] =>
        [...(quizCategories[key as QuizCategory] ?? [key, key])] as [string, string],
    };
  if (kind === 'roadmap')
    return {
      key: (item: Item) => String(item.from),
      order: levels,
      name: (key: string): [string, string] => [`Bắt đầu từ ${key}`, `Starting at ${key}`],
    };
  if (kind === 'relation')
    return {
      key: (item: Item) => String(item.level),
      order: levels,
      name: (key: string): [string, string] => [`Trình độ ${key}`, `Level ${key}`],
    };
  return {
    key: (item: Item) => String(item.topic),
    order: catalogOrder,
    name: (key: string): [string, string] => [topicVi[key] ?? key, key],
  };
}

/** Items in their groups (in the learning pages' order); words are also cut into the learners' clusters. */
function groupsOf(kind: ContentKind, list: Entry[]): Group[] {
  const { key, order, name } = grouping(kind);
  const rank = (k: string) => (order.includes(k) ? order.indexOf(k) : order.length);
  const byKey = new Map<string, Entry[]>();
  for (const entry of list) {
    const source = entry.item ?? (entry.row.data as Item | null);
    const k = source ? key(source) : '—';
    byKey.set(k, [...(byKey.get(k) ?? []), entry]);
  }
  const clustered = kind === 'word';
  return [...byKey]
    .sort(([a], [b]) => rank(a) - rank(b) || a.localeCompare(b))
    .map(([k, items]) => {
      const live = items.filter((e) => e.status === 'live');
      // Words: one cluster per 20; other kinds: one block when anything is visible.
      const count = clustered
        ? Math.ceil(live.length / STUDY_GROUP_SIZE)
        : Math.min(live.length, 1);
      return {
        key: k,
        name: name(k),
        total: items.length,
        clusters: Array.from({ length: count }, (_, i) => ({
          number: clustered ? i + 1 : 0,
          words: clustered ? live.slice(i * STUDY_GROUP_SIZE, (i + 1) * STUDY_GROUP_SIZE) : live,
        })),
        other: items.filter((e) => e.status !== 'live'),
      };
    });
}

/** Admin area for the learning content: list, add, edit, hide and restore items of every kind. */
export default function ContentManager() {
  const bi = useBi();
  const [kind, setKind] = useState<ContentKind>('word');
  const [rows, setRows] = useState<ContentRow[]>([]);
  const [search, setSearch] = useState('');
  const [editing, setEditing] = useState<{ item: Item; isNew: boolean } | null>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [confirming, setConfirming] = useState<string | null>(null);
  const [openTopics, setOpenTopics] = useState<Set<string>>(new Set());

  async function reload() {
    try {
      setRows(await fetchContentRows());
      // The learning pages read the live lists; refresh them so the admin sees the change there too.
      await loadContent(true);
    } catch {
      setError(
        bi('Không tải được tài liệu từ máy chủ.', 'Could not load content from the server.'),
      );
    }
  }
  useEffect(() => {
    void reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const all = useMemo(() => entries(kind, rows), [kind, rows]);
  const term = search.trim().toLowerCase();
  const matches = term
    ? all.filter(
        (e) =>
          e.id.toLowerCase().includes(term) ||
          (e.item && label(kind, e.item).toLowerCase().includes(term)),
      )
    : all;
  const isMatch = (e: Entry) =>
    !term ||
    e.id.toLowerCase().includes(term) ||
    (e.item !== null && label(kind, e.item).toLowerCase().includes(term));
  // Clusters come from the whole group, so a search keeps each word's real cluster number.
  const groups = useMemo(() => groupsOf(kind, all), [kind, all]);
  const groupWord =
    kind === 'structure' || kind === 'quiz'
      ? bi('nhóm', 'groups')
      : kind === 'relation' || kind === 'roadmap'
        ? bi('trình độ', 'levels')
        : bi('chủ đề', 'topics');
  const counts = Object.fromEntries(kinds.map((k) => [k.id, entries(k.id, rows).length]));
  const current = kinds.find((k) => k.id === kind)!;

  async function run(action: () => Promise<void>, done: string) {
    setError('');
    setMessage('');
    setConfirming(null);
    try {
      await action();
      await reload();
      setMessage(done);
    } catch (e) {
      setError(
        e instanceof ApiError && e.status === 400
          ? bi(
              'Máy chủ từ chối dữ liệu: thiếu trường bắt buộc hoặc mã không hợp lệ.',
              'The server rejected the item: a required field is missing or the id is invalid.',
            )
          : e instanceof ApiError && e.status === 403
            ? bi('Tài khoản này không còn quyền quản trị.', 'This account is no longer an admin.')
            : bi(
                'Không lưu được. Hãy kiểm tra kết nối rồi thử lại.',
                'Could not save. Check the connection and try again.',
              ),
      );
    }
  }

  function startNew() {
    const taken = new Set(all.map((e) => e.id));
    const template = blankItem(kind, newId(kind, taken));
    setEditing({ item: template, isNew: true });
    setMessage('');
  }

  const statusText: Record<Status, string> = {
    live: bi('Đang dùng', 'Live'),
    hidden: bi('Đã ẩn', 'Hidden'),
    invalid: bi('Lỗi dữ liệu', 'Invalid'),
  };

  const row = (e: Entry) => (
    <li key={e.id} className={e.status}>
      <div className="content-what">
        <strong>{e.item ? label(kind, e.item) : e.id}</strong>
        <small>
          <code className="content-id">{e.id}</code>
          {e.item && 'level' in e.item && (
            <span className="content-level">{String(e.item.level)}</span>
          )}
        </small>
      </div>
      <span className={`content-status ${e.status}`}>{statusText[e.status]}</span>
      <div className="content-actions">
        {e.status !== 'hidden' && (
          <button
            type="button"
            className="content-edit"
            onClick={() => {
              setEditing({ item: e.item ?? ((e.row.data as Item) || { id: e.id }), isNew: false });
              setMessage('');
            }}
          >
            <SkillIcon skill="writing" size={16} />
            {bi('Sửa', 'Edit')}
          </button>
        )}
        {e.status === 'hidden' ? (
          <button
            type="button"
            onClick={() =>
              void run(() => hideContent(kind, e.id, false), bi('Đã hiện lại.', 'Shown again.'))
            }
          >
            <SkillIcon skill="eye" size={16} />
            {bi('Hiện lại', 'Show')}
          </button>
        ) : (
          <button
            type="button"
            onClick={() =>
              void run(
                () => hideContent(kind, e.id, true),
                bi('Đã ẩn khỏi người học.', 'Hidden from learners.'),
              )
            }
          >
            <SkillIcon skill="eyeOff" size={16} />
            {bi('Ẩn', 'Hide')}
          </button>
        )}
        {confirming === e.id ? (
          <button
            type="button"
            className="danger"
            onClick={() => void run(() => deleteContent(kind, e.id), bi('Đã xoá.', 'Deleted.'))}
          >
            {bi('Xác nhận xoá vĩnh viễn', 'Confirm permanent delete')}
          </button>
        ) : (
          <button type="button" className="danger-outline" onClick={() => setConfirming(e.id)}>
            {bi('Xoá', 'Delete')}
          </button>
        )}
      </div>
    </li>
  );

  return (
    // The chosen kind's skill colour tints the header band, its tab, the group bars and the clusters.
    <section className="content-admin" aria-labelledby="content-title" data-skill={current.skill}>
      <div className="content-admin-top">
        <div className="content-admin-head">
          <h2 id="content-title">{bi('Tài liệu học tập', 'Learning content')}</h2>
          <p className="muted">
            {bi(
              'Toàn bộ bài học nằm trong cơ sở dữ liệu; người học nhận bản mới khi mở app và giữ một bản sao để học offline. Từ vựng vào cả Đua 60 giây; trợ giảng AI học bài mới ngay khi lưu (nếu hết hạn mức Gemini, bài được nạp ở lần chạy ingest sau).',
              'Every lesson lives in the database; learners get the latest when they open the app and keep a copy for offline practice. Words also feed the 60-second race; the AI tutor learns an item as soon as it is saved (if the Gemini quota is used up, the next ingest run adds it).',
            )}
          </p>
        </div>
        <div
          className="content-kinds"
          role="tablist"
          aria-label={bi('Loại tài liệu', 'Content kind')}
        >
          {kinds.map((k) => (
            <button
              key={k.id}
              type="button"
              role="tab"
              aria-selected={k.id === kind}
              data-skill={k.skill}
              onClick={() => {
                setKind(k.id);
                setEditing(null);
                setSearch('');
                setMessage('');
              }}
            >
              <span className="line-tile small" aria-hidden="true">
                <SkillIcon skill={k.icon} size={16} />
              </span>
              {bi(k.vi, k.en)}
              <small>{counts[k.id]}</small>
            </button>
          ))}
        </div>
      </div>

      {message && (
        <p role="status" className="content-message">
          {message}
        </p>
      )}
      {error && <Notice error>{error}</Notice>}

      {editing ? (
        <ContentForm
          kind={kind}
          initial={editing.item}
          isNew={editing.isNew}
          taken={new Set(all.map((e) => e.id))}
          onCancel={() => setEditing(null)}
          onSave={(item) =>
            void run(
              async () => {
                await saveContent(kind, item);
                setEditing(null);
              },
              bi(
                'Đã lưu vào cơ sở dữ liệu. Người học nhận bản mới khi mở lại app.',
                'Saved. Learners get it the next time they open the app.',
              ),
            )
          }
        />
      ) : (
        <>
          <div className="content-toolbar">
            <label>
              <span className="sr-only">{bi('Tìm tài liệu', 'Search content')}</span>
              <input
                type="search"
                placeholder={bi('Tìm theo mã, tiêu đề hoặc từ', 'Search by id, title or word')}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </label>
            <button type="button" className="primary" onClick={startNew}>
              + {bi(`Thêm ${current.vi.toLowerCase()}`, `Add ${current.en.toLowerCase()}`)}
            </button>
          </div>
          <p className="muted content-count">
            {term
              ? bi(
                  `${matches.length}/${all.length} mục khớp`,
                  `${matches.length} of ${all.length} match`,
                )
              : bi(`${all.length} mục`, `${all.length} items`)}
            {` · ${groups.length} ${groupWord}`}
            {kind === 'word' &&
              bi(
                `, mỗi cụm ${STUDY_GROUP_SIZE} từ như trang học`,
                `, ${STUDY_GROUP_SIZE}-word clusters as on the learning page`,
              )}
          </p>
          {!term && (
            <div className="content-topic-tools">
              <button
                type="button"
                onClick={() => setOpenTopics(new Set(groups.map((g) => `${kind}:${g.key}`)))}
              >
                {bi('Mở tất cả', 'Expand all')}
              </button>
              <button type="button" onClick={() => setOpenTopics(new Set())}>
                {bi('Thu gọn tất cả', 'Collapse all')}
              </button>
            </div>
          )}
          <div className="content-topics">
            {groups.map((group) => {
              const id = `${kind}:${group.key}`;
              const clusters = group.clusters
                .map((c) => ({ ...c, words: c.words.filter(isMatch) }))
                .filter((c) => c.words.length);
              const other = group.other.filter(isMatch);
              if (term && !clusters.length && !other.length) return null;
              // A search opens every group with a match.
              const open = Boolean(term) || openTopics.has(id);
              const unit = (n: number) =>
                kind === 'word' ? bi(`${n} từ`, `${n} words`) : bi(`${n} mục`, `${n} items`);
              return (
                <section key={id} className="content-topic">
                  <h3>
                    <button
                      type="button"
                      aria-expanded={open}
                      disabled={Boolean(term)}
                      onClick={() =>
                        setOpenTopics((current) => {
                          const next = new Set(current);
                          if (next.has(id)) next.delete(id);
                          else next.add(id);
                          return next;
                        })
                      }
                    >
                      <SkillIcon skill="chevron" size={16} />
                      <span className="content-topic-name">{bi(...group.name)}</span>
                      <small>
                        {unit(group.total)}
                        {kind === 'word' &&
                          bi(
                            ` · ${group.clusters.length} cụm`,
                            ` · ${group.clusters.length} clusters`,
                          )}
                      </small>
                    </button>
                  </h3>
                  {open && (
                    <div className="content-clusters">
                      {clusters.map((cluster) =>
                        cluster.number ? (
                          <section key={cluster.number} className="content-cluster">
                            <h4>
                              {bi(`Cụm ${cluster.number}`, `Cluster ${cluster.number}`)}{' '}
                              <small>{unit(cluster.words.length)}</small>
                            </h4>
                            <ul className="content-list">{cluster.words.map(row)}</ul>
                          </section>
                        ) : (
                          <ul key="all" className="content-list">
                            {cluster.words.map(row)}
                          </ul>
                        ),
                      )}
                      {other.length > 0 && (
                        <section className="content-cluster">
                          <h4>
                            {bi('Đã ẩn hoặc lỗi dữ liệu', 'Hidden or invalid')}{' '}
                            <small>{unit(other.length)}</small>
                          </h4>
                          <ul className="content-list">{other.map(row)}</ul>
                        </section>
                      )}
                    </div>
                  )}
                </section>
              );
            })}
          </div>
        </>
      )}
    </section>
  );
}
