import { useEffect, useMemo, useRef, useState } from 'react';
import { SpeakButton } from '../../components/SpeakButton';
import { levelSchema, type Level } from '../../data/schema';
import { wordRelations, type WordRelation } from '../../data/wordRelations';
import { useBi } from '../../i18n';
import {
  createRelationSession,
  filterRelations,
  saveRelationAnswer,
  type RelationMode,
  type RelationQuestion,
} from '../../services/wordRelations';
import '../../styles/word-relations.css';

const levelNames: Record<string, [string, string]> = {
  A1: ['Mới bắt đầu', 'Beginner'],
  A2: ['Cơ bản', 'Elementary'],
  B1: ['Trung cấp', 'Intermediate'],
  B2: ['Trung cấp cao', 'Upper intermediate'],
  C1: ['Nâng cao', 'Advanced'],
  C2: ['Thành thạo', 'Proficient'],
};

const partsOfSpeech: Record<WordRelation['pos'], [string, string]> = {
  adjective: ['Tính từ', 'Adjective'],
  verb: ['Động từ', 'Verb'],
  noun: ['Danh từ', 'Noun'],
  adverb: ['Trạng từ', 'Adverb'],
};

export default function WordRelations() {
  const bi = useBi();
  const [level, setLevel] = useState<Level | 'all'>('all');
  const [search, setSearch] = useState('');
  const [mode, setMode] = useState<RelationMode>('mixed');
  const [page, setPage] = useState(0);
  const [session, setSession] = useState<RelationQuestion[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [checked, setChecked] = useState(false);
  const [correct, setCorrect] = useState(0);
  const [completed, setCompleted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [saveError, setSaveError] = useState(false);
  const saving = useRef(false);
  const started = useRef(0);
  const questionHeading = useRef<HTMLHeadingElement>(null);
  const libraryHeading = useRef<HTMLHeadingElement>(null);
  const resultsHeading = useRef<HTMLHeadingElement>(null);
  const filtered = useMemo(() => filterRelations(wordRelations, level, search), [level, search]);
  const pages = Math.ceil(filtered.length / 12);
  const visible = filtered.slice(page * 12, page * 12 + 12);
  const question = session[index];
  const matched = question?.answer === answer;

  useEffect(() => {
    if (session.length) questionHeading.current?.focus();
  }, [index, session, completed]);

  function start() {
    const next = createRelationSession(filtered, mode, 10);
    if (!next.length) return;
    setSession(next);
    setIndex(0);
    setAnswer('');
    setChecked(false);
    setCorrect(0);
    setCompleted(false);
    setSaveError(false);
    started.current = Date.now();
  }

  async function check() {
    if (!question || !answer || checked || saving.current) return;
    saving.current = true;
    setBusy(true);
    setSaveError(false);
    try {
      await saveRelationAnswer(question, answer, started.current);
      setChecked(true);
      setCorrect((value) => value + Number(answer === question.answer));
    } catch {
      setSaveError(true);
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }

  function nextQuestion() {
    if (!checked || saving.current) return;
    if (index + 1 === session.length) {
      setCompleted(true);
      return;
    }
    setIndex((value) => value + 1);
    setAnswer('');
    setChecked(false);
    setSaveError(false);
    started.current = Date.now();
  }

  function backToLibrary() {
    if (saving.current) return;
    setSession([]);
    setCompleted(false);
    requestAnimationFrame(() => libraryHeading.current?.focus());
  }

  function changePage(next: number) {
    setPage(next);
    requestAnimationFrame(() => {
      resultsHeading.current?.focus();
    });
  }

  if (session.length && completed) {
    return (
      <section className="word-relations">
        <div className="relations-complete panel">
          <h2 ref={questionHeading} tabIndex={-1}>
            {bi('Đã hoàn thành lượt luyện!', 'Practice complete!')}
          </h2>
          <p className="relations-result-count">
            {correct}
            <span> / {session.length}</span>
          </p>
          <p>{bi('câu trả lời đúng', 'correct answers')}</p>
          <p className="muted">
            {bi(
              'Tất cả câu trả lời trong lượt này đã được lưu vào lịch sử học.',
              'Every answer in this session has been saved to your learning history.',
            )}
          </p>
          <div className="relations-actions">
            <button type="button" className="primary" onClick={start}>
              {bi('Luyện thêm một lượt', 'Practice again')}
            </button>
            <button type="button" onClick={backToLibrary}>
              {bi('Về thư viện từ', 'Back to word library')}
            </button>
          </div>
        </div>
      </section>
    );
  }

  if (session.length && question) {
    return (
      <section className="word-relations">
        <div className="relations-session-header">
          <button type="button" onClick={backToLibrary} disabled={busy}>
            {bi('← Về thư viện từ', '← Back to word library')}
          </button>
          <span>
            {bi('Câu', 'Question')} {index + 1} / {session.length}
          </span>
        </div>
        <progress
          className="relations-progress"
          value={index + Number(checked)}
          max={session.length}
          aria-label={bi('Tiến độ lượt luyện', 'Session progress')}
        />
        <div className="relations-question panel">
          <div className="relations-question-meta">
            <span className="relations-level-badge" data-level={question.entry.level}>
              {question.entry.level}
            </span>
            <span className={`relations-kind relations-kind-${question.kind}`}>
              {question.kind === 'synonym'
                ? bi('≈ Từ đồng nghĩa', '≈ Synonym')
                : bi('↔ Từ trái nghĩa', '↔ Antonym')}
            </span>
          </div>
          <h2 ref={questionHeading} tabIndex={-1}>
            {question.kind === 'synonym'
              ? bi('Từ nào có nghĩa gần nhất?', 'Which word is closest in meaning?')
              : bi('Từ nào có nghĩa trái ngược?', 'Which word has the opposite meaning?')}
          </h2>
          <p className="relations-target" lang="en">
            {question.entry.word}
          </p>
          <p className="relations-sense">{bi(question.entry.meaning, question.entry.definition)}</p>
          <blockquote lang="en">{question.entry.example}</blockquote>
          <fieldset className="relations-choices" disabled={busy || checked}>
            <legend>
              {bi(
                'Chọn một đáp án theo nghĩa và ngữ cảnh trên',
                'Choose one answer for the meaning and context above',
              )}
            </legend>
            {question.options.map((option, optionIndex) => (
              <label className="relations-option" key={option} data-selected={answer === option}>
                <input
                  type="radio"
                  name="relation-answer"
                  value={option}
                  checked={answer === option}
                  onChange={() => setAnswer(option)}
                />
                <span className="relations-option-letter" aria-hidden="true">
                  {String.fromCharCode(65 + optionIndex)}
                </span>
                <span lang="en">{option}</span>
              </label>
            ))}
          </fieldset>
          {saveError && (
            <p className="notice error" role="alert">
              {bi(
                'Chưa lưu được câu trả lời. Hãy thử lại; câu hỏi vẫn được giữ nguyên.',
                'Your answer could not be saved. Please retry; this question has been kept.',
              )}
            </p>
          )}
          {checked && (
            <div className="relations-feedback" role="status" data-correct={matched}>
              <strong>
                {matched
                  ? bi('Chính xác! Đã lưu kết quả.', 'Correct! Result saved.')
                  : bi('Đã lưu kết quả. Cùng xem lại nhé.', 'Result saved. Let’s review it.')}
              </strong>
              <p>
                {bi('Đáp án:', 'Answer:')} <b lang="en">{question.answer}</b>
              </p>
              <p>{bi(question.entry.usageNote.vi, question.entry.usageNote.en)}</p>
            </div>
          )}
          <div className="relations-question-actions">
            {checked ? (
              <button type="button" className="primary" onClick={nextQuestion}>
                {index + 1 === session.length
                  ? bi('Xem kết quả →', 'See results →')
                  : bi('Tiếp tục →', 'Continue →')}
              </button>
            ) : (
              <button
                type="button"
                className="primary"
                disabled={!answer || busy}
                onClick={() => void check()}
              >
                {busy
                  ? bi('Đang lưu…', 'Saving…')
                  : saveError
                    ? bi('Thử lưu lại', 'Retry saving')
                    : bi('Kiểm tra & lưu', 'Check & save')}
              </button>
            )}
            <span className="muted">
              {bi('Đã lưu', 'Saved')}: {index + Number(checked)} / {session.length}
            </span>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="word-relations">
      <div className="relations-head">
        <h2 ref={libraryHeading} tabIndex={-1}>
          {bi('Đồng nghĩa & trái nghĩa', 'Synonyms & antonyms')}
        </h2>
        <p className="muted">
          {bi(
            `${wordRelations.length} mục từ · A1–C2 · Học theo một nghĩa cụ thể, có ví dụ`,
            `${wordRelations.length} entries · A1–C2 · One meaning at a time, with examples`,
          )}
        </p>
      </div>

      <section
        className="relations-levels-section"
        aria-label={bi('Chọn mức độ CEFR', 'Choose a CEFR level')}
      >
        <div className="relations-section-title">
          <h3>{bi('Bắt đầu ở mức phù hợp', 'Start at your level')}</h3>
          <button
            type="button"
            className="relations-all-levels"
            aria-pressed={level === 'all'}
            onClick={() => {
              setLevel('all');
              setPage(0);
            }}
          >
            {bi('Tất cả mức độ', 'All levels')}
          </button>
        </div>
        <div className="relations-levels">
          {levelSchema.options.map((item) => (
            <button
              className="relations-level"
              type="button"
              key={item}
              data-level={item}
              aria-pressed={level === item}
              onClick={() => {
                setLevel(item);
                setPage(0);
              }}
            >
              <strong>{item}</strong>
              <span>{bi(...levelNames[item])}</span>
              <small>
                {wordRelations.filter((entry) => entry.level === item).length}{' '}
                {bi('mục từ', 'entries')}
              </small>
            </button>
          ))}
        </div>
        <p className="relations-level-hint">
          {bi(
            'Mức bài học tham khảo; các từ trong cùng nhóm có thể khác độ khó.',
            'Suggested lesson levels; words in one group can differ in difficulty.',
          )}
        </p>
        <details className="relations-level-note">
          <summary>{bi('Hiểu về cách chia mức độ A1–C2', 'About the A1–C2 levels')}</summary>
          <p>
            {bi(
              'A1–C2 là các mức năng lực của khung CEFR. Trong thư viện này, mức độ là phân loại biên soạn cho nghĩa đang học, không phải danh sách từ chính thức của một kỳ thi hay quy đổi điểm IELTS/TOEIC.',
              'A1–C2 are proficiency levels in the CEFR. Here, levels are editorial classifications of the meaning being studied, not an official exam word list or an IELTS/TOEIC score conversion.',
            )}
          </p>
          <p>
            {bi(
              'Từ gần nghĩa không luôn thay thế được nhau. Hãy đọc ví dụ và ghi chú trước khi dùng.',
              'Near-synonyms are not always interchangeable. Read the examples and usage notes before using them.',
            )}{' '}
            <a
              href="https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions"
              target="_blank"
              rel="noreferrer"
            >
              {bi('Xem mô tả CEFR chính thức', 'Official CEFR descriptions')}
            </a>
          </p>
        </details>
      </section>

      <div className="relations-toolbar">
        <label className="relations-search">
          <span>{bi('Tìm từ hoặc nghĩa', 'Search words or meanings')}</span>
          <input
            type="search"
            value={search}
            placeholder={bi('Ví dụ: happy, sad, vui…', 'Try happy, sad, vui…')}
            onChange={(event) => {
              setSearch(event.target.value);
              setPage(0);
            }}
          />
        </label>
        <label>
          <span>{bi('Loại quan hệ từ', 'Word relationship')}</span>
          <select value={mode} onChange={(event) => setMode(event.target.value as RelationMode)}>
            <option value="mixed">{bi('Cả hai loại', 'Both types')}</option>
            <option value="synonym">{bi('Đồng nghĩa', 'Synonyms')}</option>
            <option value="antonym">{bi('Trái nghĩa', 'Antonyms')}</option>
          </select>
        </label>
        <button className="primary" type="button" onClick={start} disabled={!filtered.length}>
          {bi('Luyện', 'Practice')} {Math.min(10, filtered.length)} {bi('câu →', 'questions →')}
        </button>
      </div>
      <div className="relations-library-heading">
        <h3 ref={resultsHeading} tabIndex={-1}>
          {bi('Thư viện kết nối từ', 'Word connection library')}
        </h3>
        <span role="status">
          {filtered.length} {bi('mục từ', 'entries')} · {level === 'all' ? 'A1–C2' : level}
        </span>
      </div>
      {filtered.length ? (
        <div className="relations-grid">
          {visible.map((entry) => (
            <article className="relations-card" key={entry.id}>
              <div className="relations-card-top">
                <span className="relations-level-badge" data-level={entry.level}>
                  {entry.level}
                </span>
                <span>{bi(...partsOfSpeech[entry.pos])}</span>
                <SpeakButton text={entry.word} />
              </div>
              <h4 lang="en">{entry.word}</h4>
              {bi(entry.meaning, '') && (
                <p className="relations-word-meaning">{bi(entry.meaning, '')}</p>
              )}
              <p className="relations-word-definition" lang="en">
                {entry.definition}
              </p>
              <p className="relations-example" lang="en">
                {entry.example}
              </p>
              <div className="relations-pair-grid" data-mode={mode}>
                {(['synonym', 'antonym'] as const)
                  .filter((kind) => mode === 'mixed' || mode === kind)
                  .map((kind) => (
                    <div className={`relations-pair relations-pair-${kind}`} key={kind}>
                      <p className="relations-pair-label">
                        {kind === 'synonym'
                          ? bi('≈ ĐỒNG NGHĨA', '≈ SYNONYM')
                          : bi('↔ TRÁI NGHĨA', '↔ ANTONYM')}
                      </p>
                      {(kind === 'synonym' ? entry.synonyms : entry.antonyms).map((related) => (
                        <div key={related.word}>
                          <strong lang="en">{related.word}</strong>
                          {bi(related.meaning, '') && <p>{bi(related.meaning, '')}</p>}
                          <p className="relations-related-example" lang="en">
                            {related.example}
                          </p>
                        </div>
                      ))}
                    </div>
                  ))}
              </div>
              <p className="relations-usage">
                <b>{bi('Dùng đúng:', 'Usage:')}</b> {bi(entry.usageNote.vi, entry.usageNote.en)}
              </p>
            </article>
          ))}
        </div>
      ) : (
        <div className="relations-empty panel">
          <span aria-hidden="true">⌕</span>
          <h3>{bi('Chưa tìm thấy từ phù hợp', 'No matching words')}</h3>
          <p>
            {bi(
              'Thử một từ khác hoặc chọn tất cả mức độ.',
              'Try a different word or choose all levels.',
            )}
          </p>
          <button
            type="button"
            onClick={() => {
              setSearch('');
              setLevel('all');
              setPage(0);
            }}
          >
            {bi('Xóa bộ lọc', 'Clear filters')}
          </button>
        </div>
      )}
      {pages > 1 && (
        <nav
          className="relations-pagination"
          aria-label={bi('Phân trang quan hệ từ', 'Word relationship pagination')}
        >
          <button type="button" disabled={page === 0} onClick={() => changePage(page - 1)}>
            {bi('← Trang trước', '← Previous')}
          </button>
          <span>
            {bi('Trang', 'Page')} {page + 1} / {pages}
          </span>
          <button type="button" disabled={page + 1 === pages} onClick={() => changePage(page + 1)}>
            {bi('Trang sau →', 'Next →')}
          </button>
        </nav>
      )}
    </section>
  );
}
