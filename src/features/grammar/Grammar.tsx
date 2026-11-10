import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import SkillIcon from '../../components/SkillIcon';
import Tenses from './Tenses';
import { useBi, useT } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
import { structures, tenses } from '../../data/content';
import { structureGroups, type Structure, type StructureGroup } from '../../data/schema';
import { logAttempt } from '../../services/storage';

export const groupLabels: Record<StructureGroup, [string, string]> = {
  linking: ['Nối câu: nguyên nhân, mục đích, nhượng bộ', 'Linking: cause, purpose, contrast'],
  degree: ['Quá… / đủ…', 'Too… / enough…'],
  'to-v': ['Động từ + to-V', 'Verb + to-V'],
  'v-ing': ['Động từ + V-ing', 'Verb + V-ing'],
  'sb-do': ['Động từ + ai + làm gì', 'Verb + someone + do'],
  change: ['to-V hay V-ing (đổi nghĩa)', 'to-V or V-ing (meaning changes)'],
  'ing-phrases': ['Cụm cố định + V-ing', 'Fixed phrases + V-ing'],
  habits: ['Thói quen, sở thích, khả năng', 'Habits, likes and abilities'],
  compare: ['So sánh và lựa chọn', 'Comparing and preferring'],
  time: ['Thời gian và thì hoàn thành', 'Time and perfect tenses'],
  'it-there': ['Câu với It / There', 'It / There sentences'],
  academic: ['Nguyên nhân – kết quả (văn học thuật)', 'Cause and effect (academic)'],
};
const QUIZ_SIZE = 10;

const shuffle = <T,>(items: readonly T[]) =>
  items
    .map((item) => ({ item, order: Math.random() }))
    .sort((a, b) => a.order - b.order)
    .map(({ item }) => item);

type Question = { structure: Structure; choices: string[] };

/** The example with the structure marked (learn) or blanked out (practice). */
function Example({ structure, blank = false }: { structure: Structure; blank?: boolean }) {
  const bi = useBi();
  const [before, after] = structure.example.split(structure.key);
  return (
    <p className="structure-example" lang="en">
      {before}
      {blank ? (
        <span className="structure-blank">
          <span aria-hidden="true">_____</span>
          <span className="sr-only">{bi('(chỗ trống)', '(blank)')}</span>
        </span>
      ) : (
        <mark>{structure.key}</mark>
      )}
      {after}
    </p>
  );
}

/** The 100 sentence patterns: browse and search them, then fill the gaps. */
function Patterns() {
  const bi = useBi();
  const [mode, setMode] = useState<'learn' | 'practice'>('learn');
  const [group, setGroup] = useState<StructureGroup | 'all'>('all');
  const [query, setQuery] = useState('');
  const label = (g: StructureGroup | 'all') =>
    g === 'all' ? bi('Tất cả nhóm', 'All groups') : bi(...groupLabels[g]);

  const inGroup = useMemo(
    () => structures.filter((s) => group === 'all' || s.group === group),
    [group],
  );
  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q
      ? inGroup.filter((s) =>
          [s.formula, s.meaning, s.example, s.translation].some((text) =>
            text.toLowerCase().includes(q),
          ),
        )
      : inGroup;
  }, [inGroup, query]);

  // Practice state
  const [quiz, setQuiz] = useState<Question[]>([]);
  const [index, setIndex] = useState(0);
  const [picked, setPicked] = useState<string | null>(null);
  const [wrong, setWrong] = useState<Structure[]>([]);
  const [started, setStarted] = useState(0);
  const [done, setDone] = useState(false);
  const [saveFailed, setSaveFailed] = useState(false);

  function startPractice() {
    setQuiz(
      shuffle(inGroup)
        .slice(0, QUIZ_SIZE)
        .map((structure) => ({
          structure,
          choices: shuffle([structure.key, ...structure.options]),
        })),
    );
    setIndex(0);
    setPicked(null);
    setWrong([]);
    setStarted(Date.now());
    setDone(false);
    setSaveFailed(false);
    setMode('practice');
  }

  function choose(choice: string) {
    if (picked) return;
    setPicked(choice);
    const { structure } = quiz[index];
    if (choice !== structure.key) setWrong((list) => [...list, structure]);
  }

  async function next() {
    if (index + 1 < quiz.length) {
      setIndex(index + 1);
      setPicked(null);
      return;
    }
    setDone(true);
    const score = Math.round(((quiz.length - wrong.length) / quiz.length) * 100);
    try {
      await logAttempt(
        'grammar',
        score,
        started,
        `${bi('Cấu trúc câu', 'Sentence patterns')} · ${label(group)}`,
      );
    } catch {
      setSaveFailed(true);
    }
  }

  const controls = (
    <div className="filters">
      <label>
        {bi('Nhóm cấu trúc', 'Pattern group')}
        <select value={group} onChange={(e) => setGroup(e.target.value as StructureGroup | 'all')}>
          <option value="all">{label('all')}</option>
          {structureGroups.map((g) => (
            <option key={g} value={g}>
              {label(g)}
            </option>
          ))}
        </select>
      </label>
      <label>
        {bi('Tìm cấu trúc', 'Search patterns')}
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={bi('Ví dụ: enjoy, mặc dù, than…', 'For example: enjoy, although, than…')}
        />
      </label>
    </div>
  );

  const tabs = (
    <div className="tabs">
      <button aria-pressed={mode === 'learn'} onClick={() => setMode('learn')}>
        {bi('Học', 'Learn')}
      </button>
      <button aria-pressed={mode === 'practice'} onClick={startPractice}>
        {bi('Luyện tập', 'Practice')}
      </button>
    </div>
  );

  if (mode === 'learn')
    return (
      <>
        {tabs}
        {controls}
        <p className="muted" role="status">
          {bi(
            `Đang hiện ${shown.length} / ${structures.length} cấu trúc`,
            `Showing ${shown.length} of ${structures.length} patterns`,
          )}
        </p>
        <div className="structure-list">
          {shown.map((s) => (
            <article className="panel structure-card" key={s.id}>
              <div className="structure-card-top">
                <span className="lesson-number">#{Number(s.id.slice(1))}</span>
                <span className="badge">{label(s.group)}</span>
              </div>
              <h2 lang="en">{s.formula}</h2>
              <p className="structure-meaning">{s.meaning}</p>
              <div className="structure-example-row">
                <Example structure={s} />
                <SpeakButton text={s.example} />
              </div>
              <p className="muted">{s.translation}</p>
            </article>
          ))}
        </div>
      </>
    );

  const question = quiz[index];
  const correct = quiz.length - wrong.length;
  return (
    <>
      {tabs}
      {done ? (
        <section className="panel space-y-4" aria-labelledby="grammar-result">
          <h2 id="grammar-result">
            {bi('Kết quả', 'Result')}: {correct} / {quiz.length}
          </h2>
          {wrong.length > 0 ? (
            <>
              <p>{bi('Ôn lại các cấu trúc bạn trả lời sai:', 'Review the patterns you missed:')}</p>
              <ul className="structure-review">
                {wrong.map((s) => (
                  <li key={s.id}>
                    <strong lang="en">{s.formula}</strong> · {s.meaning}
                    <Example structure={s} />
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p>{bi('Tuyệt vời, bạn trả lời đúng hết!', 'Great, all correct!')}</p>
          )}
          {saveFailed && (
            <Notice error>{bi('Không lưu được kết quả.', 'Could not save the result.')}</Notice>
          )}
          <div className="actions">
            <button className="primary" onClick={startPractice}>
              {bi('Làm lại', 'Try again')}
            </button>
            <button onClick={() => setMode('learn')}>
              {bi('Quay lại học', 'Back to learning')}
            </button>
          </div>
        </section>
      ) : question ? (
        <section className="panel flashcard" aria-labelledby="grammar-question">
          <p className="muted" id="grammar-question">
            {bi('Câu', 'Question')} {index + 1} / {quiz.length} · {label(question.structure.group)}
          </p>
          <p className="structure-meaning">
            {bi('Gợi ý nghĩa', 'Meaning')}: {question.structure.translation}
          </p>
          <Example structure={question.structure} blank />
          <div className="choice-grid">
            {question.choices.map((choice) => {
              const mark = !picked
                ? ''
                : choice === question.structure.key
                  ? 'right'
                  : choice === picked
                    ? 'wrong'
                    : '';
              return (
                <button
                  key={choice}
                  lang="en"
                  className={mark}
                  disabled={picked !== null}
                  onClick={() => choose(choice)}
                >
                  {choice}
                  {mark === 'right' && ' ✓'}
                  {mark === 'wrong' && ' ✗'}
                </button>
              );
            })}
          </div>
          <p role="status" aria-live="polite">
            {picked &&
              (picked === question.structure.key
                ? bi('Đúng!', 'Correct!')
                : `${bi('Chưa đúng. Đáp án', 'Not quite. Answer')}: ${question.structure.key}`)}
          </p>
          {picked && (
            <>
              <p>
                <strong lang="en">{question.structure.formula}</strong> ·{' '}
                {question.structure.meaning}
              </p>
              <div className="actions">
                <button className="primary" onClick={() => void next()}>
                  {index + 1 < quiz.length
                    ? bi('Câu tiếp', 'Next')
                    : bi('Xem kết quả', 'See result')}
                </button>
              </div>
            </>
          )}
        </section>
      ) : null}
    </>
  );
}

/** Grammar: the sentence patterns and every tense, as two parts of one page (?part=tenses). */
export default function Grammar() {
  const bi = useBi();
  const t = useT();
  const [params, setParams] = useSearchParams();
  const part = params.get('part') === 'tenses' ? 'tenses' : 'patterns';
  const parts = [
    {
      id: 'patterns',
      icon: 'grammar',
      vi: 'Cấu trúc câu',
      en: 'Sentence patterns',
      noteVi: `${structures.length} mẫu câu kèm ví dụ, học rồi luyện điền chỗ trống`,
      noteEn: `${structures.length} patterns with examples, then gap-fill practice`,
    },
    {
      id: 'tenses',
      icon: 'roadmap',
      vi: 'Các thì',
      en: 'Tenses',
      noteVi: `${tenses.length} thì: công thức, cách dùng, dấu hiệu và luyện nhanh`,
      noteEn: `${tenses.length} tenses: form, uses, signal words and a quick check`,
    },
  ] as const;
  return (
    <>
      <PageTitle
        title={t('grammar')}
        description={bi(
          'Cấu trúc câu và toàn bộ các thì trong tiếng Anh: xem công thức và ví dụ, rồi luyện tập.',
          'Sentence patterns and every English tense: read the form and examples, then practise.',
        )}
      />
      <div
        className="grammar-parts"
        role="tablist"
        aria-label={bi('Phần ngữ pháp', 'Grammar parts')}
      >
        {parts.map((p) => (
          <button
            key={p.id}
            type="button"
            role="tab"
            aria-selected={p.id === part}
            onClick={() => setParams(p.id === 'tenses' ? { part: 'tenses' } : {})}
          >
            <span className="line-tile" aria-hidden="true">
              <SkillIcon skill={p.icon} size={20} />
            </span>
            <span>
              <strong>{bi(p.vi, p.en)}</strong>
              <small>{bi(p.noteVi, p.noteEn)}</small>
            </span>
          </button>
        ))}
      </div>
      {part === 'tenses' ? <Tenses /> : <Patterns />}
    </>
  );
}
