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
}: {
  questions: Question[];
  answers: Record<string, string>;
  onChange: (id: string, value: string) => void;
  submitted: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const [current, setCurrent] = useState(0);
  const i = Math.min(current, questions.length - 1);
  const q = questions[i];
  const answered = questions.filter((item) => answers[item.id]?.trim()).length;
  if (!q) return null;
  return (
    <div className="question-pager">
      <div className="question-stations-head">
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
        <legend className="font-semibold">
          {i + 1}. {q.prompt}
        </legend>
        {q.type === 'choice' || q.type === 'tfng' ? (
          (q.type === 'tfng' ? ['True', 'False', 'Not Given'] : (q.options ?? [])).map((option) => (
            <label key={option}>
              <input
                type="radio"
                name={q.id}
                value={option}
                checked={answers[q.id] === option}
                disabled={submitted}
                onChange={() => onChange(q.id, option)}
              />
              {option}
            </label>
          ))
        ) : (
          <label>
            {t('answer')}
            <input
              disabled={submitted}
              value={answers[q.id] ?? ''}
              onChange={(e) => onChange(q.id, e.target.value)}
            />
          </label>
        )}
        {submitted && (
          <div className={`notice ${isCorrect(q, answers[q.id] ?? '') ? 'right' : 'error'}`}>
            <strong>
              {isCorrect(q, answers[q.id] ?? '') ? '✓' : '✕'} {q.answers[0]}
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
    </div>
  );
}
