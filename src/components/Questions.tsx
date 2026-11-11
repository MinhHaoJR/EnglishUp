import { useState } from 'react';
import { useBi, useT } from '../i18n';
import type { Question } from '../data/schema';
export function normalizeAnswer(text: string) {
  return text
    .toLowerCase()
    .trim()
    .replace(/[.,!?;:]+$/g, '')
    .replace(/\s+/g, ' ');
}
export function isCorrect(q: Question, answer: string) {
  return q.answers.some((a) => normalizeAnswer(a) === normalizeAnswer(answer));
}

/** One question at a time, with a row of stations showing which are answered (and, once checked, right). */
export function Questions({
  questions,
  answers,
  onChange,
  submitted,
  onCheck,
  checking = false,
}: {
  questions: Question[];
  answers: Record<string, string>;
  onChange: (id: string, value: string) => void;
  submitted: boolean;
  /** Shows the check button under the questions; it unlocks once every question has an answer. */
  onCheck?: () => void;
  checking?: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const [current, setCurrent] = useState(0);
  const i = Math.min(current, questions.length - 1);
  const q = questions[i];
  const answered = questions.filter((item) => answers[item.id]?.trim()).length;
  const left = questions.length - answered;
  if (!q) return null;
  const right = isCorrect(q, answers[q.id] ?? '');
  return (
    <div className="question-pager">
      <div className="question-head">
        <strong className="question-count">
          {bi('Câu', 'Question')} {i + 1}
          <span>/{questions.length}</span>
        </strong>
        <span className="muted">
          {bi(
            `Đã trả lời ${answered}/${questions.length}`,
            `${answered}/${questions.length} answered`,
          )}
        </span>
      </div>
      <nav className="question-stations" aria-label={bi('Các câu hỏi', 'Questions')}>
        {questions.map((item, n) => {
          const done = !!answers[item.id]?.trim();
          const state = submitted
            ? isCorrect(item, answers[item.id] ?? '')
              ? 'right'
              : 'wrong'
            : done
              ? 'done'
              : '';
          const status = submitted
            ? state === 'right'
              ? bi('đúng', 'right')
              : bi('sai', 'wrong')
            : done
              ? bi('đã trả lời', 'answered')
              : bi('chưa trả lời', 'not answered');
          return (
            <button
              key={item.id}
              type="button"
              className={`question-station ${state}`}
              aria-current={n === i ? 'step' : undefined}
              aria-label={`${bi('Câu', 'Question')} ${n + 1}, ${status}`}
              onClick={() => setCurrent(n)}
            >
              {n + 1}
            </button>
          );
        })}
      </nav>
      <fieldset className="question" key={q.id}>
        <legend className="question-prompt">
          <span className="sr-only">{i + 1}. </span>
          {q.prompt}
        </legend>
        {q.type === 'choice' || q.type === 'tfng' ? (
          <div className="question-options">
            {(q.type === 'tfng' ? ['True', 'False', 'Not Given'] : (q.options ?? [])).map(
              (option, n) => {
                const chosen = answers[q.id] === option;
                const mark = !submitted
                  ? ''
                  : q.answers.some((a) => normalizeAnswer(a) === normalizeAnswer(option))
                    ? 'right'
                    : chosen
                      ? 'wrong'
                      : '';
                return (
                  <label key={option} className={`question-option ${mark}`}>
                    <input
                      type="radio"
                      name={q.id}
                      value={option}
                      checked={chosen}
                      disabled={submitted}
                      onChange={() => onChange(q.id, option)}
                    />
                    <span className="option-key" aria-hidden="true">
                      {String.fromCharCode(65 + n)}
                    </span>
                    <span>{option}</span>
                  </label>
                );
              },
            )}
          </div>
        ) : (
          <label className="question-short">
            {t('answer')}
            <input
              disabled={submitted}
              value={answers[q.id] ?? ''}
              onChange={(e) => onChange(q.id, e.target.value)}
            />
          </label>
        )}
        {submitted && (
          <div className={`notice ${right ? 'right' : 'error'}`}>
            <strong>
              {right ? '✓' : '✕'} {q.answers[0]}
            </strong>
            <p>
              {t('explanation')}: {q.explanation}
            </p>
            <p className="muted">
              {t('evidence')}: “{q.evidence}”
            </p>
          </div>
        )}
      </fieldset>
      <div className="question-nav">
        <button type="button" disabled={i === 0} onClick={() => setCurrent(i - 1)}>
          ← {bi('Câu trước', 'Previous question')}
        </button>
        <button
          type="button"
          disabled={i === questions.length - 1}
          onClick={() => setCurrent(i + 1)}
        >
          {bi('Câu tiếp', 'Next question')} →
        </button>
      </div>
      {onCheck && !submitted && (
        <div className="question-check">
          <button className="primary" disabled={checking || left > 0} onClick={onCheck}>
            {t('check')}
          </button>
          <span className="muted" role="status">
            {left > 0
              ? bi(`Còn ${left} câu chưa trả lời.`, `${left} still to answer.`)
              : bi('Đã trả lời hết, bấm để xem kết quả.', 'All answered: check your result.')}
          </span>
        </div>
      )}
    </div>
  );
}
