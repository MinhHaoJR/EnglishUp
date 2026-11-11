import { LessonBrowser, byLevel } from '../../components/LessonBrowser';
import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import { useState } from 'react';
import { readings } from '../../data/content';
import type { ReadingLesson } from '../../data/schema';
import { useT, useBi } from '../../i18n';
import { Notice, PageTitle, useFiltered, useTimer } from '../../components/shared';
import { DictionaryText } from '../../components/DictionaryText';
import { Questions, isCorrect } from '../../components/Questions';
import { logAttempt } from '../../services/storage';
function ReadingSession({
  lesson,
  onBack,
  onContinue,
  hasNext,
}: {
  lesson: ReadingLesson;
  onBack: () => void;
  onContinue: () => void;
  hasNext: boolean;
}) {
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
        title={lesson.title}
        meta={`${lesson.level} · ${lesson.topic}`}
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
          <Questions
            questions={lesson.questions}
            answers={answers}
            submitted={submitted}
            onChange={(id, v) => setAnswers({ ...answers, [id]: v })}
            checking={busy}
            onCheck={() => {
              setBusy(true);
              void logAttempt('reading', score, start, lesson.title)
                .then(() => {
                  setSubmitted(true);
                  if (readingSeconds === undefined) setReadingSeconds(Math.max(1, seconds));
                })
                .catch(() => setError(t('error')))
                .finally(() => setBusy(false));
            }}
          />
          {submitted && (
            <Notice>
              {t('result')} · {score}%
            </Notice>
          )}
          {submitted && <LessonContinue onContinue={onContinue} hasNext={hasNext} />}
          {error && <Notice error>{error}</Notice>}
        </section>
      </div>
    </>
  );
}
export default function Reading() {
  const t = useT();
  const bi = useBi();
  const all = byLevel(readings);
  const filtered = useFiltered(all);
  const [active, setActive] = useState<ReadingLesson>();
  if (active)
    return (
      <ReadingSession
        key={active.id}
        lesson={active}
        onBack={() => setActive(undefined)}
        onContinue={() => setActive(nextLesson(filtered, active))}
        hasNext={!!nextLesson(filtered, active)}
      />
    );
  return (
    <>
      <PageTitle title={t('reading')} />
      <LessonBrowser
        skill="reading"
        all={all}
        onOpen={setActive}
        describe={(r) => ({
          preview: `${r.text.slice(0, 125)}…`,
          meta: `${r.text.split(/\s+/).length} ${t('words')} · ${r.questions.length} ${bi('câu hỏi', 'questions')}`,
        })}
      />
    </>
  );
}
