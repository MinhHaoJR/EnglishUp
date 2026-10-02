import { useState } from 'react';
import { readings } from '../../data/content';
import type { ReadingLesson } from '../../data/schema';
import { useT, useBi } from '../../i18n';
import { Empty, Filters, Notice, PageTitle, useFiltered, useTimer } from '../../components/shared';
import { DictionaryText } from '../../components/DictionaryText';
import { Questions, isCorrect } from '../../components/Questions';
import { logAttempt } from '../../services/storage';
function ReadingSession({ lesson, onBack }: { lesson: ReadingLesson; onBack: () => void }) {
  const t = useT();
  const bi = useBi();
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [readingSeconds, setReadingSeconds] = useState<number>();
  const { start, seconds } = useTimer(!submitted);
  const count = lesson.text.split(/\s+/).length;
  const score = Math.round(
    (lesson.questions.filter((q) => isCorrect(q, answers[q.id] ?? '')).length /
      lesson.questions.length) *
      100,
  );
  return (
    <>
      <button className="mb-6" onClick={onBack}>
        ← {t('back')}
      </button>
      <PageTitle
        eyebrow={`${lesson.level} · ${lesson.topic}`}
        title={lesson.title}
        description={`${count} ${t('words')} · ${seconds}s`}
      />
      <div className="split">
        <article className="panel">
          <p className="muted mb-4">
            {bi('Bấm vào một từ để tra nghĩa hoặc lưu.', 'Tap a word to look it up or save it.')}
          </p>
          <DictionaryText text={lesson.text} />
          <button
            className="mt-5"
            disabled={readingSeconds !== undefined}
            onClick={() => setReadingSeconds(Math.max(1, seconds))}
          >
            {bi('Đã đọc xong', 'Finished reading')}
          </button>
          {readingSeconds !== undefined && (
            <p className="muted">
              {readingSeconds}s · {Math.round(count / (readingSeconds / 60))} WPM
            </p>
          )}
        </article>
        <section className="panel">
          <h2>{bi('Đọc hiểu', 'Check your understanding')}</h2>
          <Questions
            questions={lesson.questions}
            answers={answers}
            submitted={submitted}
            onChange={(id, v) => setAnswers({ ...answers, [id]: v })}
          />
          {submitted ? (
            <Notice>
              {t('result')} · {score}%
            </Notice>
          ) : (
            <button
              className="primary mt-5"
              disabled={busy || lesson.questions.some((q) => !answers[q.id]?.trim())}
              onClick={() => {
                setBusy(true);
                void logAttempt('reading', score, start, lesson.title)
                  .then(() => {
                    setSubmitted(true);
                    if (readingSeconds === undefined) setReadingSeconds(Math.max(1, seconds));
                  })
                  .catch(() => setError(t('error')))
                  .finally(() => setBusy(false));
              }}
            >
              {t('check')}
            </button>
          )}
          {error && <Notice error>{error}</Notice>}
        </section>
      </div>
    </>
  );
}
export default function Reading() {
  const t = useT();
  const bi = useBi();
  const filtered = useFiltered(readings);
  const [active, setActive] = useState<ReadingLesson>();
  if (active)
    return <ReadingSession key={active.id} lesson={active} onBack={() => setActive(undefined)} />;
  return (
    <>
      <PageTitle
        eyebrow={bi('MỖI TRANG ĐỌC, THÊM MỘT GÓC NHÌN', 'A NEW PERSPECTIVE, ONE PAGE AT A TIME')}
        title={t('reading')}
        description={bi(
          'Những câu chuyện nhỏ, những góc nhìn mới.',
          'Small stories. Fresh perspectives.',
        )}
      />
      <Filters />
      {!filtered.length ? (
        <Empty />
      ) : (
        <div className="lesson-grid">
          {filtered.map((r, i) => (
            <article className="panel lesson-card" key={r.id}>
              <span className="lesson-number">0{i + 1} / READING</span>
              <span className="badge">
                {r.level} · {r.topic}
              </span>
              <h2>{r.title}</h2>
              <p className="muted">{r.text.slice(0, 125)}…</p>
              <span className="muted">
                {r.text.split(/\s+/).length} {t('words')} · 5 {bi('câu hỏi', 'questions')}
              </span>
              <button className="primary" onClick={() => setActive(r)}>
                {t('start')} →
              </button>
            </article>
          ))}
        </div>
      )}
    </>
  );
}
