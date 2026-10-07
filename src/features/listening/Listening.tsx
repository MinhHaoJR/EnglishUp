import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import { useEffect, useState } from 'react';
import { listenings, dictations } from '../../data/content';
import type { ListeningLesson } from '../../data/schema';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import { Filters, PageTitle, Notice, Empty, useFiltered, useTimer } from '../../components/shared';
import { Questions, isCorrect } from '../../components/Questions';
import { DictionaryText } from '../../components/DictionaryText';
import { WordDiff } from '../../components/WordDiff';
import { alignWords } from '../../services/diff';
import { speakLines, stopSpeech } from '../../services/speech';
import { logAttempt } from '../../services/storage';
function AudioPlayer({
  lines,
  reveal,
}: {
  lines: { speaker: string; text: string }[];
  reveal: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const settings = useApp((s) => s.settings);
  const [speed, setSpeed] = useState(1);
  const [error, setError] = useState('');
  const sentences = lines.flatMap((line) =>
    (line.text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) ?? [line.text]).map((text) => ({
      speaker: line.speaker,
      text: text.trim(),
    })),
  );
  useEffect(() => () => stopSpeech(), []);
  const play = (items: typeof lines) =>
    speakLines(
      items,
      { ...settings, rate: settings.rate * speed },
      () =>
        setError(
          bi(
            'Không phát được âm thanh. Kiểm tra giọng đọc hoặc thử trình duyệt khác.',
            'Audio unavailable. Check installed voices or try another browser.',
          ),
        ),
      [...new Set(lines.map((line) => line.speaker))],
    );
  return (
    <section className="audio-player">
      <div className="audio-art" aria-hidden="true">
        <span>▂</span>
        <span>▅</span>
        <span>▇</span>
        <span>▃</span>
        <span>▆</span>
        <span>█</span>
        <span>▅</span>
        <span>▂</span>
      </div>
      <div className="actions">
        <button className="primary" onClick={() => play(sentences)}>
          ▶ {t('listen')}
        </button>
        <button onClick={stopSpeech}>■ {t('stop')}</button>
        <label>
          {bi('Tốc độ bài nghe', 'Playback speed')}
          <select value={speed} onChange={(e) => setSpeed(Number(e.target.value))}>
            {[0.75, 1, 1.25].map((n) => (
              <option value={n} key={n}>
                {n}×
              </option>
            ))}
          </select>
        </label>
      </div>
      <p className="muted mt-4">
        {bi('Nghe lại từng câu', 'Replay a sentence')} · {settings.accent}
      </p>
      <div className="actions mt-2">
        {sentences.map((line, i) => (
          <button
            key={i}
            onClick={() => play([line])}
            aria-label={`${bi('Nghe câu', 'Play sentence')} ${i + 1}`}
          >
            {i + 1}
            {reveal ? ` · ${line.speaker}` : ''}
          </button>
        ))}
      </div>
      {error && <Notice error>{error}</Notice>}
    </section>
  );
}
function ListeningSession({
  lesson,
  onBack,
  onContinue,
  hasNext,
}: {
  lesson: ListeningLesson;
  onBack: () => void;
  onContinue: () => void;
  hasNext: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const settings = useApp((s) => s.settings);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const { start } = useTimer(!submitted);
  const score = Math.round(
    (lesson.questions.filter((q) => isCorrect(q, answers[q.id] ?? '')).length /
      lesson.questions.length) *
      100,
  );
  return (
    <>
      <button className="mb-5" onClick={onBack}>
        ← {t('back')}
      </button>
      <PageTitle title={lesson.title} eyebrow={`${lesson.level} · ${lesson.topic}`} />
      <div className="split">
        <section className="panel">
          <AudioPlayer lines={lesson.lines} reveal={submitted || settings.transcript} />
          {submitted || settings.transcript ? (
            <div className="mt-6">
              <h2>{bi('Bản chép lời', 'Transcript')}</h2>
              {lesson.lines.map((line, i) => (
                <div className="mt-4" key={i}>
                  <strong className="muted">{line.speaker}</strong>
                  <DictionaryText text={line.text} />
                </div>
              ))}
            </div>
          ) : (
            <p className="notice">
              {bi(
                'Bản chép lời sẽ mở sau khi bạn trả lời.',
                'The transcript unlocks after you answer.',
              )}
            </p>
          )}
        </section>
        <section className="panel">
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
                void logAttempt('listening', score, start, lesson.title)
                  .then(() => setSubmitted(true))
                  .catch(() => setError(t('error')))
                  .finally(() => setBusy(false));
              }}
            >
              {t('check')}
            </button>
          )}
          {submitted && <LessonContinue onContinue={onContinue} hasNext={hasNext} />}
          {error && <Notice error>{error}</Notice>}
        </section>
      </div>
    </>
  );
}
function DictationSession({
  item,
  onBack,
  onContinue,
  hasNext,
}: {
  item: (typeof dictations)[number];
  onBack: () => void;
  onContinue: () => void;
  hasNext: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const show = useApp((s) => s.settings.transcript);
  const [answer, setAnswer] = useState('');
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const { start } = useTimer(!done);
  return (
    <>
      <button className="mb-5" onClick={onBack}>
        ← {t('back')}
      </button>
      <PageTitle
        title={bi('Nghe và chép lại', 'Listen and write')}
        eyebrow={`${item.level} · ${item.topic}`}
      />
      <section className="panel">
        <AudioPlayer lines={[{ speaker: 'Narrator', text: item.text }]} reveal={done || show} />
        {show && !done && <DictionaryText text={item.text} />}
        <form
          className="mt-6"
          onSubmit={(e) => {
            e.preventDefault();
            setBusy(true);
            void logAttempt(
              'listening',
              alignWords(item.text, answer).score,
              start,
              `Dictation ${item.id}`,
            )
              .then(() => setDone(true))
              .catch(() => setError(t('error')))
              .finally(() => setBusy(false));
          }}
        >
          <label>
            {t('answer')}
            <textarea
              maxLength={3000}
              value={answer}
              disabled={done}
              onChange={(e) => setAnswer(e.target.value)}
            />
          </label>
          <button className="primary mt-4" disabled={done || busy || !answer.trim()}>
            {t('check')}
          </button>
        </form>
        {done && (
          <>
            <WordDiff target={item.text} actual={answer} />
            <DictionaryText text={item.text} />
            <Notice>{t('result')}</Notice>
            <LessonContinue onContinue={onContinue} hasNext={hasNext} />
          </>
        )}
        {error && <Notice error>{error}</Notice>}
      </section>
    </>
  );
}
export default function Listening() {
  const t = useT();
  const bi = useBi();
  const lessons = useFiltered(listenings);
  const sentences = useFiltered(dictations);
  const [tab, setTab] = useState('lessons');
  const [active, setActive] = useState<ListeningLesson>();
  const [dictation, setDictation] = useState<(typeof dictations)[number]>();
  if (active)
    return (
      <ListeningSession
        key={active.id}
        lesson={active}
        onBack={() => setActive(undefined)}
        onContinue={() => setActive(nextLesson(lessons, active))}
        hasNext={!!nextLesson(lessons, active)}
      />
    );
  if (dictation)
    return (
      <DictationSession
        key={dictation.id}
        item={dictation}
        onBack={() => setDictation(undefined)}
        onContinue={() => setDictation(nextLesson(sentences, dictation))}
        hasNext={!!nextLesson(sentences, dictation)}
      />
    );
  return (
    <>
      <PageTitle
        eyebrow={bi('LẮNG NGHE TIẾNG ANH ĐỜI THƯỜNG', 'TUNE IN TO EVERYDAY ENGLISH')}
        title={t('listening')}
        description={bi(
          'Lắng nghe, hiểu ý, rồi thử lại theo nhịp của bạn.',
          'Listen, understand, and replay at your own pace.',
        )}
      />
      <div className="tabs">
        <button aria-pressed={tab === 'lessons'} onClick={() => setTab('lessons')}>
          {bi('Hội thoại & bài nói', 'Dialogues & talks')}
        </button>
        <button aria-pressed={tab === 'dictation'} onClick={() => setTab('dictation')}>
          {bi('Chép chính tả', 'Dictation')}
        </button>
      </div>
      <Filters />
      {tab === 'lessons' ? (
        lessons.length ? (
          <div className="lesson-grid">
            {lessons.map((l, i) => (
              <article key={l.id} className="panel lesson-card">
                <span className="lesson-number">0{i + 1} / LISTENING</span>
                <span className="badge">
                  {l.level} · {l.topic}
                </span>
                <h2>{l.title}</h2>
                <p className="muted">
                  {l.lines.length} {bi('lượt nói', 'speaking turns')} · {l.questions.length}{' '}
                  {bi('câu hỏi', 'questions')}
                </p>
                <button className="primary" onClick={() => setActive(l)}>
                  {t('start')} →
                </button>
              </article>
            ))}
          </div>
        ) : (
          <Empty />
        )
      ) : sentences.length ? (
        <div className="lesson-grid">
          {sentences.map((d, i) => (
            <article key={d.id} className="panel lesson-card">
              <span className="badge">
                {d.level} · {d.topic}
              </span>
              <h2>
                {bi('Câu', 'Sentence')} {i + 1}
              </h2>
              <p className="muted">
                {bi(
                  'Nghe và gõ lại. Nhận phản hồi từng từ.',
                  'Listen and type. Get feedback on each word.',
                )}
              </p>
              <button className="primary" onClick={() => setDictation(d)}>
                {t('start')}
              </button>
            </article>
          ))}
        </div>
      ) : (
        <Empty />
      )}
    </>
  );
}
