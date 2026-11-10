import { useEffect, useMemo, useState } from 'react';
import { useBi, topicVi } from '../../i18n';
import { Notice } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { levelSchema, type Word } from '../../data/schema';
import { ApiError } from '../../services/auth';
import {
  contentKinds,
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
];
const PAGE = 50;

/** One line that names an item in the list, whatever its kind. */
function label(kind: ContentKind, item: Item) {
  if (kind === 'word' || kind === 'relation')
    return `${String(item.word)} — ${String(item.meaning)}`;
  if (kind === 'translation') return String((item.en as string[] | undefined)?.[0]);
  if (kind === 'structure') return String(item.formula);
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
    // The first item of the kind is the template, so the editor shows the expected shape.
    const first = all.find((e) => e.item)?.item ?? {};
    const template = { ...first, id: newId(kind, taken) } as Item;
    setEditing({ item: template, isNew: true });
    setMessage('');
  }

  const statusText: Record<Status, string> = {
    live: bi('Đang dùng', 'Live'),
    hidden: bi('Đã ẩn', 'Hidden'),
    invalid: bi('Lỗi dữ liệu', 'Invalid'),
  };

  return (
    <section className="content-admin" aria-labelledby="content-title">
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

      {message && (
        <p role="status" className="content-message">
          {message}
        </p>
      )}
      {error && <Notice error>{error}</Notice>}

      {editing ? (
        <Editor
          kind={kind}
          initial={editing.item}
          isNew={editing.isNew}
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
            {matches.length > PAGE
              ? bi(
                  `Hiển thị ${PAGE}/${matches.length} mục; hãy tìm để thu hẹp.`,
                  `Showing ${PAGE} of ${matches.length}; search to narrow it down.`,
                )
              : bi(`${matches.length} mục`, `${matches.length} items`)}
          </p>
          <ul className="content-list">
            {matches.slice(0, PAGE).map((e) => (
              <li key={e.id} className={e.status}>
                <div className="content-what">
                  <strong>{e.item ? label(kind, e.item) : e.id}</strong>
                  <small>
                    <code>{e.id}</code>
                    {e.item && 'level' in e.item && ` · ${String(e.item.level)}`}
                    {e.item && 'topic' in e.item && ` · ${String(e.item.topic)}`}
                  </small>
                </div>
                <span className={`content-status ${e.status}`}>{statusText[e.status]}</span>
                <div className="content-actions">
                  {e.status !== 'hidden' && (
                    <button
                      type="button"
                      onClick={() => {
                        setEditing({
                          item: e.item ?? ((e.row.data as Item) || { id: e.id }),
                          isNew: false,
                        });
                        setMessage('');
                      }}
                    >
                      {bi('Sửa', 'Edit')}
                    </button>
                  )}
                  {e.status === 'hidden' ? (
                    <button
                      type="button"
                      onClick={() =>
                        void run(
                          () => hideContent(kind, e.id, false),
                          bi('Đã hiện lại.', 'Shown again.'),
                        )
                      }
                    >
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
                      {bi('Ẩn', 'Hide')}
                    </button>
                  )}
                  {confirming === e.id ? (
                    <button
                      type="button"
                      className="danger"
                      onClick={() =>
                        void run(() => deleteContent(kind, e.id), bi('Đã xoá.', 'Deleted.'))
                      }
                    >
                      {bi('Xác nhận xoá vĩnh viễn', 'Confirm permanent delete')}
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="danger-outline"
                      onClick={() => setConfirming(e.id)}
                    >
                      {bi('Xoá', 'Delete')}
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

/** A form for words (the common case); a JSON editor checked live against the app's schema for the rest. */
function Editor({
  kind,
  initial,
  isNew,
  onSave,
  onCancel,
}: {
  kind: ContentKind;
  initial: Item;
  isNew: boolean;
  onSave: (item: Item) => void;
  onCancel: () => void;
}) {
  const bi = useBi();
  const [text, setText] = useState(() => JSON.stringify(initial, null, 2));
  const [word, setWord] = useState(() => initial as unknown as Word);

  let value: unknown = null;
  let syntax = '';
  if (kind === 'word') value = word;
  else
    try {
      value = JSON.parse(text);
    } catch (e) {
      syntax = e instanceof Error ? e.message : String(e);
    }
  const check = syntax ? null : contentKinds[kind].schema.safeParse(value);
  const issues = syntax
    ? [bi(`JSON chưa đúng cú pháp: ${syntax}`, `The JSON is not valid: ${syntax}`)]
    : check && !check.success
      ? check.error.issues.map((i) => `${i.path.join('.') || '(item)'}: ${i.message}`)
      : [];
  const idChanged = !isNew && (value as Item | null)?.id !== initial.id;
  if (idChanged)
    issues.push(
      bi(
        'Không đổi mã khi sửa; hãy thêm mục mới nếu cần mã khác.',
        'Keep the id when editing; add a new item for a different id.',
      ),
    );

  const topicIds = [...new Set(contentKinds.word.items.map((w) => w.topic))].sort();
  const field = (key: keyof Word, labelText: string, long = false) => (
    <label>
      {labelText}
      {long ? (
        <textarea
          value={String(word[key] ?? '')}
          onChange={(e) => setWord({ ...word, [key]: e.target.value })}
        />
      ) : (
        <input
          value={String(word[key] ?? '')}
          onChange={(e) => setWord({ ...word, [key]: e.target.value })}
        />
      )}
    </label>
  );

  return (
    <form
      className="content-editor"
      onSubmit={(event) => {
        event.preventDefault();
        if (check?.success && !idChanged) onSave(check.data as Item);
      }}
    >
      <h3>
        {isNew ? bi('Thêm mục mới', 'New item') : bi('Sửa mục', 'Edit item')}{' '}
        <code>{initial.id}</code>
      </h3>
      {kind === 'word' ? (
        <div className="content-word">
          {field('word', bi('Từ', 'Word'))}
          {field('ipa', bi('Phiên âm', 'IPA'))}
          {field('pos', bi('Từ loại', 'Part of speech'))}
          {field('meaning', bi('Nghĩa tiếng Việt', 'Vietnamese meaning'))}
          {field('definition', bi('Định nghĩa tiếng Anh', 'English definition'), true)}
          <label>
            {bi('Ví dụ 1', 'Example 1')}
            <input
              value={word.examples[0] ?? ''}
              onChange={(e) =>
                setWord({ ...word, examples: [e.target.value, ...word.examples.slice(1)] })
              }
            />
          </label>
          <label>
            {bi('Ví dụ 2 (không bắt buộc)', 'Example 2 (optional)')}
            <input
              value={word.examples[1] ?? ''}
              onChange={(e) =>
                setWord({
                  ...word,
                  examples: e.target.value
                    ? [word.examples[0] ?? '', e.target.value]
                    : [word.examples[0] ?? ''],
                })
              }
            />
          </label>
          <label>
            {bi('Trình độ', 'Level')}
            <select
              value={word.level}
              onChange={(e) => setWord({ ...word, level: e.target.value as Word['level'] })}
            >
              {levelSchema.options.map((l) => (
                <option key={l}>{l}</option>
              ))}
            </select>
          </label>
          <label>
            {bi('Chủ đề', 'Topic')}
            <select
              value={word.topic}
              onChange={(e) => setWord({ ...word, topic: e.target.value })}
            >
              {topicIds.map((t) => (
                <option key={t} value={t}>
                  {bi(topicVi[t] ?? t, t)}
                </option>
              ))}
            </select>
          </label>
        </div>
      ) : (
        <label className="content-json">
          {bi(
            'Nội dung (JSON theo cấu trúc của các bài cùng loại)',
            'Content (JSON in the same shape as the other items of this kind)',
          )}
          <textarea
            spellCheck={false}
            value={text}
            onChange={(e) => setText(e.target.value)}
            aria-describedby="content-issues"
          />
        </label>
      )}
      <div id="content-issues" aria-live="polite">
        {issues.length ? (
          <ul className="content-issues">
            {issues.map((issue) => (
              <li key={issue}>{issue}</li>
            ))}
          </ul>
        ) : (
          <p className="content-ok">
            <SkillIcon skill="check" size={16} />{' '}
            {bi('Hợp lệ với cấu trúc của ứng dụng.', 'Valid for the app.')}
          </p>
        )}
      </div>
      <div className="actions">
        <button className="primary" disabled={issues.length > 0}>
          {bi('Lưu', 'Save')}
        </button>
        <button type="button" onClick={onCancel}>
          {bi('Huỷ', 'Cancel')}
        </button>
      </div>
    </form>
  );
}
