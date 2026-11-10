import { useState } from 'react';
import { useBi, topicVi } from '../../i18n';
import SkillIcon from '../../components/SkillIcon';
import { levelSchema, structureGroups, type StructureGroup } from '../../data/schema';
import { topicSections } from '../../data/topicSections';
import { contentKinds, type ContentKind } from '../../services/content';
import { groupLabels } from '../grammar/Grammar';

type Item = { id: string } & Record<string, unknown>;
type Value = Record<string, unknown>;
type Label = [string, string];

/**
 * One form field. `key` is a path into the item ("synonyms.0.word"). A list is one string per line;
 * rows repeat a group of fields (dialogue lines, questions) with add and remove buttons.
 */
type Field = {
  key: string;
  label: Label;
  type: 'text' | 'long' | 'number' | 'select' | 'list' | 'rows';
  options?: readonly string[];
  optionLabel?: (option: string) => Label;
  /** Shown only when this returns true for the value the field belongs to. */
  showIf?: (value: Value) => boolean;
  fields?: Field[];
  /** A new row for `rows`, given the item and the number of rows so far. */
  template?: (item: Value, count: number) => Value;
  /** Rows a new item starts with (the schema's minimum). */
  min?: number;
  wide?: boolean;
  /** May stay empty (the IPA of a word); every other text must be filled, as the server requires. */
  optional?: boolean;
  /** A tall box for a whole passage. */
  tall?: boolean;
};

const topics: string[] = topicSections.flatMap((section) => [...section.topics]);
const level: Field = {
  key: 'level',
  label: ['Trình độ', 'Level'],
  type: 'select',
  options: levelSchema.options,
};
const topic: Field = {
  key: 'topic',
  label: ['Chủ đề', 'Topic'],
  type: 'select',
  options: topics,
  optionLabel: (t) => [topicVi[t] ?? t, t],
};
const title: Field = { key: 'title', label: ['Tiêu đề', 'Title'], type: 'text', wide: true };

const questionTypes: Record<string, Label> = {
  choice: ['Trắc nghiệm', 'Multiple choice'],
  tfng: ['Đúng / Sai / Không có thông tin', 'True / False / Not Given'],
  short: ['Trả lời ngắn', 'Short answer'],
  blank: ['Điền chỗ trống', 'Fill in the blank'],
};
const questions = (min: number): Field => ({
  key: 'questions',
  label: [`Câu hỏi (ít nhất ${min})`, `Questions (at least ${min})`],
  type: 'rows',
  min,
  template: (item, count) => ({
    id: `${String(item.id)}q${count + 1}`,
    type: 'choice',
    prompt: '',
    options: ['', ''],
    answers: [''],
    explanation: '',
    evidence: '',
  }),
  fields: [
    {
      key: 'type',
      label: ['Dạng câu hỏi', 'Question type'],
      type: 'select',
      options: Object.keys(questionTypes),
      optionLabel: (t) => questionTypes[t],
    },
    { key: 'prompt', label: ['Câu hỏi', 'Prompt'], type: 'long', wide: true },
    {
      key: 'options',
      label: ['Các lựa chọn (mỗi dòng một)', 'Options (one per line)'],
      type: 'list',
      showIf: (q) => q.type === 'choice',
    },
    {
      key: 'answers',
      label: [
        'Đáp án chấp nhận (mỗi dòng một; dạng Đúng/Sai dùng True, False hoặc Not Given)',
        'Accepted answers (one per line; True, False or Not Given for that type)',
      ],
      type: 'list',
    },
    { key: 'explanation', label: ['Giải thích', 'Explanation'], type: 'long' },
    {
      key: 'evidence',
      label: ['Câu làm bằng chứng trong bài', 'Evidence from the text'],
      type: 'long',
    },
  ],
});
const related = (key: 'synonyms' | 'antonyms', vi: string, en: string): Field[] => [
  { key: `${key}.0.word`, label: [`${vi}: từ`, `${en}: word`], type: 'text' },
  { key: `${key}.0.meaning`, label: [`${vi}: nghĩa`, `${en}: meaning`], type: 'text' },
  { key: `${key}.0.example`, label: [`${vi}: ví dụ`, `${en}: example`], type: 'long', wide: true },
];

/** The fields of each kind, matching the app's schemas in data/schema.ts and data/wordRelations.ts. */
const specs: Record<ContentKind, Field[]> = {
  word: [
    { key: 'word', label: ['Từ', 'Word'], type: 'text' },
    {
      key: 'ipa',
      label: ['Phiên âm (không bắt buộc)', 'IPA (optional)'],
      type: 'text',
      optional: true,
    },
    { key: 'pos', label: ['Từ loại', 'Part of speech'], type: 'text' },
    { key: 'meaning', label: ['Nghĩa tiếng Việt', 'Vietnamese meaning'], type: 'text' },
    {
      key: 'definition',
      label: ['Định nghĩa tiếng Anh', 'English definition'],
      type: 'long',
      wide: true,
    },
    {
      key: 'examples',
      label: ['Ví dụ (mỗi dòng một câu, tối đa 2)', 'Examples (one per line, up to 2)'],
      type: 'list',
      wide: true,
    },
    level,
    topic,
  ],
  structure: [
    {
      key: 'group',
      label: ['Nhóm ngữ pháp', 'Grammar group'],
      type: 'select',
      options: structureGroups,
      optionLabel: (g) => groupLabels[g as StructureGroup],
    },
    { key: 'formula', label: ['Công thức', 'Formula'], type: 'text' },
    { key: 'meaning', label: ['Ý nghĩa', 'Meaning'], type: 'text', wide: true },
    { key: 'example', label: ['Câu ví dụ', 'Example sentence'], type: 'long', wide: true },
    {
      key: 'key',
      label: [
        'Phần được che khi luyện (nằm trong câu ví dụ)',
        'Part blanked in the quiz (inside the example)',
      ],
      type: 'text',
    },
    {
      key: 'options',
      label: ['Hai đáp án sai (mỗi dòng một)', 'Two wrong answers (one per line)'],
      type: 'list',
    },
    {
      key: 'translation',
      label: ['Bản dịch câu ví dụ', 'Translation of the example'],
      type: 'long',
      wide: true,
    },
  ],
  reading: [
    title,
    level,
    topic,
    { key: 'text', label: ['Bài đọc', 'Passage'], type: 'long', wide: true, tall: true },
    questions(5),
  ],
  listening: [
    title,
    level,
    topic,
    {
      key: 'lines',
      label: ['Lời thoại', 'Dialogue lines'],
      type: 'rows',
      min: 2,
      template: () => ({ speaker: '', text: '' }),
      fields: [
        { key: 'speaker', label: ['Người nói', 'Speaker'], type: 'text' },
        { key: 'text', label: ['Câu nói', 'Line'], type: 'long', wide: true },
      ],
    },
    questions(4),
  ],
  dictation: [
    { key: 'text', label: ['Câu chép chính tả', 'Dictation sentence'], type: 'long', wide: true },
    level,
    topic,
  ],
  speaking: [
    title,
    level,
    topic,
    {
      key: 'mode',
      label: ['Hình thức', 'Mode'],
      type: 'select',
      options: ['read', 'talk'],
      optionLabel: (m) =>
        m === 'read' ? ['Đọc nhại theo mẫu', 'Read aloud'] : ['Nói tự do', 'Free talk'],
    },
    { key: 'text', label: ['Nội dung nói', 'Text to say'], type: 'long', wide: true },
    {
      key: 'cues',
      label: ['Gợi ý (mỗi dòng một)', 'Cues (one per line)'],
      type: 'list',
      wide: true,
    },
  ],
  writing: [
    title,
    level,
    topic,
    {
      key: 'genre',
      label: ['Thể loại', 'Genre'],
      type: 'select',
      options: ['email', 'opinion', 'description', 'story'],
      optionLabel: (g) =>
        ({
          email: ['Thư / email', 'Email'],
          opinion: ['Nêu ý kiến', 'Opinion'],
          description: ['Miêu tả', 'Description'],
          story: ['Kể chuyện', 'Story'],
        })[g] as Label,
    },
    { key: 'prompt', label: ['Đề bài', 'Prompt'], type: 'long', wide: true },
    { key: 'minWords', label: ['Số từ tối thiểu', 'Minimum words'], type: 'number' },
    { key: 'maxWords', label: ['Số từ tối đa', 'Maximum words'], type: 'number' },
    {
      key: 'checklist',
      label: [
        'Tiêu chí tự kiểm tra (mỗi dòng một, ít nhất 3)',
        'Checklist (one per line, at least 3)',
      ],
      type: 'list',
      wide: true,
    },
  ],
  translation: [
    level,
    topic,
    {
      key: 'en',
      label: [
        'Câu tiếng Anh (dòng đầu là câu chính, các dòng sau là cách nói khác)',
        'English (first line is the prompt, others are accepted alternatives)',
      ],
      type: 'list',
      wide: true,
    },
    {
      key: 'vi',
      label: [
        'Câu tiếng Việt (dòng đầu là câu chính, các dòng sau là cách nói khác)',
        'Vietnamese (first line is the prompt, others are accepted alternatives)',
      ],
      type: 'list',
      wide: true,
    },
  ],
  relation: [
    { key: 'word', label: ['Từ chính', 'Headword'], type: 'text' },
    {
      key: 'pos',
      label: ['Từ loại', 'Part of speech'],
      type: 'select',
      options: ['adjective', 'verb', 'noun', 'adverb'],
      optionLabel: (p) =>
        ({
          adjective: ['Tính từ', 'Adjective'],
          verb: ['Động từ', 'Verb'],
          noun: ['Danh từ', 'Noun'],
          adverb: ['Trạng từ', 'Adverb'],
        })[p] as Label,
    },
    level,
    { key: 'meaning', label: ['Nghĩa tiếng Việt', 'Vietnamese meaning'], type: 'text' },
    {
      key: 'definition',
      label: ['Định nghĩa tiếng Anh', 'English definition'],
      type: 'long',
      wide: true,
    },
    { key: 'example', label: ['Câu ví dụ', 'Example'], type: 'long', wide: true },
    ...related('synonyms', 'Đồng nghĩa', 'Synonym'),
    ...related('antonyms', 'Trái nghĩa', 'Antonym'),
    {
      key: 'usageNote.vi',
      label: ['Ghi chú cách dùng (tiếng Việt)', 'Usage note (Vietnamese)'],
      type: 'long',
      wide: true,
    },
    {
      key: 'usageNote.en',
      label: ['Ghi chú cách dùng (tiếng Anh)', 'Usage note (English)'],
      type: 'long',
      wide: true,
    },
  ],
};

const pathOf = (key: string) =>
  key.split('.').map((part) => (/^\d+$/.test(part) ? Number(part) : part));
const getAt = (value: unknown, path: (string | number)[]): unknown =>
  path.reduce<unknown>(
    (at, part) => (at as Record<string | number, unknown> | undefined)?.[part],
    value,
  );
function setAt(value: unknown, path: (string | number)[], next: unknown): unknown {
  if (!path.length) return next;
  const [part, ...rest] = path;
  const base = (
    Array.isArray(value)
      ? [...value]
      : value && typeof value === 'object'
        ? { ...value }
        : typeof part === 'number'
          ? []
          : {}
  ) as Record<string | number, unknown>;
  base[part] = setAt(base[part], rest, next);
  return base;
}

/** An empty item of the kind: blank texts, the first option of each choice and the minimum rows. */
export function blankItem(kind: ContentKind, id: string): Item {
  const fill = (fields: Field[], into: Value, item: Value): Value =>
    fields.reduce<Value>((value, f) => {
      const path = pathOf(f.key);
      const empty =
        f.type === 'rows'
          ? Array.from({ length: f.min ?? 0 }, (_, i) =>
              fill(f.fields!, f.template!(item, i), item),
            )
          : f.type === 'list'
            ? ['']
            : f.type === 'select'
              ? f.options![0]
              : '';
      return setAt(value, path, empty) as Value;
    }, into);
  const item = { id };
  return fill(specs[kind], item, item) as Item;
}

/** Labels of the texts left empty (each line of a list counts), with row numbers for repeated rows. */
function missing(fields: Field[], value: Value, prefix: Label = ['', '']): Label[] {
  const blank = (text: unknown) => typeof text !== 'string' || text.trim() === '';
  return fields
    .filter((f) => !f.optional && (!f.showIf || f.showIf(value)))
    .flatMap((f): Label[] => {
      const current = getAt(value, pathOf(f.key));
      const name: Label = [prefix[0] + f.label[0], prefix[1] + f.label[1]];
      if (f.type === 'rows')
        return (Array.isArray(current) ? (current as Value[]) : []).flatMap((row, i) =>
          missing(f.fields!, row, [`${name[0]} ${i + 1} › `, `${name[1]} ${i + 1} › `]),
        );
      if (f.type === 'list')
        return !Array.isArray(current) || !current.length || current.some(blank) ? [name] : [];
      if (f.type === 'number') return typeof current === 'number' ? [] : [name];
      return blank(current) ? [name] : [];
    });
}

/** The fields of one value (an item, a question or a dialogue line), rendered from the spec. */
function Fields({
  fields,
  value,
  item,
  onChange,
}: {
  fields: Field[];
  value: Value;
  item: Value;
  onChange: (value: Value) => void;
}) {
  const bi = useBi();
  return (
    <div className="content-fields">
      {fields
        .filter((f) => !f.showIf || f.showIf(value))
        .map((f) => {
          const path = pathOf(f.key);
          const current = getAt(value, path);
          const set = (next: unknown) => onChange(setAt(value, path, next) as Value);
          const name = bi(...f.label);
          const wide = f.wide || f.type === 'rows' ? 'wide' : undefined;
          if (f.type === 'rows') {
            const rows = Array.isArray(current) ? (current as Value[]) : [];
            return (
              <fieldset key={f.key} className="content-rows wide">
                <legend>{name}</legend>
                {rows.map((row, index) => (
                  <fieldset key={index} className="content-row">
                    <legend>{bi(`Mục ${index + 1}`, `Item ${index + 1}`)}</legend>
                    <Fields
                      fields={f.fields!}
                      value={row}
                      item={item}
                      onChange={(next) => set(rows.map((r, i) => (i === index ? next : r)))}
                    />
                    <button
                      type="button"
                      className="danger-outline"
                      onClick={() => set(rows.filter((_, i) => i !== index))}
                    >
                      {bi(`Bỏ mục ${index + 1}`, `Remove item ${index + 1}`)}
                    </button>
                  </fieldset>
                ))}
                <button
                  type="button"
                  onClick={() => set([...rows, f.template!(item, rows.length)])}
                >
                  + {bi('Thêm mục', 'Add item')}
                </button>
              </fieldset>
            );
          }
          return (
            <label key={f.key} className={wide}>
              {name}
              {f.type === 'select' ? (
                <select value={String(current ?? '')} onChange={(e) => set(e.target.value)}>
                  {!f.options!.includes(String(current)) && (
                    <option value={String(current ?? '')}>{String(current ?? '—')}</option>
                  )}
                  {f.options!.map((option) => (
                    <option key={option} value={option}>
                      {f.optionLabel ? bi(...f.optionLabel(option)) : option}
                    </option>
                  ))}
                </select>
              ) : f.type === 'long' ? (
                <textarea
                  className={f.tall ? 'tall' : undefined}
                  value={String(current ?? '')}
                  onChange={(e) => set(e.target.value)}
                />
              ) : f.type === 'list' ? (
                <textarea
                  value={Array.isArray(current) ? current.join('\n') : ''}
                  // Splitting keeps empty lines, so typing a new line round-trips exactly.
                  onChange={(e) => set(e.target.value.split('\n'))}
                />
              ) : (
                <input
                  type={f.type === 'number' ? 'number' : 'text'}
                  value={String(current ?? '')}
                  onChange={(e) =>
                    set(
                      f.type === 'number' && e.target.value !== ''
                        ? Number(e.target.value)
                        : e.target.value,
                    )
                  }
                />
              )}
            </label>
          );
        })}
    </div>
  );
}

/** Adds or edits one item with a form for its kind, checked live against the app's schema before saving. */
export default function ContentForm({
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
  const [draft, setDraft] = useState<Value>(initial);
  const check = contentKinds[kind].schema.safeParse(draft);
  const empty = missing(specs[kind], draft).map((name) =>
    bi(`Chưa điền: ${name[0]}`, `Not filled: ${name[1]}`),
  );
  const issues = [
    ...empty,
    ...(check.success
      ? []
      : check.error.issues.map(
          (i) => `${i.path.join('.') || bi('(toàn mục)', '(item)')}: ${i.message}`,
        )),
  ];

  return (
    <form
      className="content-editor"
      onSubmit={(event) => {
        event.preventDefault();
        if (check.success) onSave(check.data as Item);
      }}
    >
      <h3>
        {isNew ? bi('Thêm mục mới', 'New item') : bi('Sửa mục', 'Edit item')}{' '}
        <code>{initial.id}</code>
      </h3>
      <Fields fields={specs[kind]} value={draft} item={draft} onChange={setDraft} />
      <div id="content-issues" aria-live="polite">
        {issues.length ? (
          <ul className="content-issues">
            {/* A blank lesson has dozens of empty fields; the first few say what to do next. */}
            {issues.slice(0, 8).map((issue) => (
              <li key={issue}>{issue}</li>
            ))}
            {issues.length > 8 && (
              <li>{bi(`… và ${issues.length - 8} mục khác`, `… and ${issues.length - 8} more`)}</li>
            )}
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
          {bi('Lưu vào cơ sở dữ liệu', 'Save to the database')}
        </button>
        <button type="button" onClick={onCancel}>
          {bi('Huỷ', 'Cancel')}
        </button>
      </div>
    </form>
  );
}
