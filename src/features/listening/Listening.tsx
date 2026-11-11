import { LessonBrowser, byLevel } from '../../components/LessonBrowser';
import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import { useEffect, useState } from 'react';
import { listenings, dictations } from '../../data/content';
import type { ListeningLesson } from '../../data/schema';
import { useApp } from '../../app/store';
import SkillIcon from '../../components/SkillIcon';
import { useT, useBi } from '../../i18n';
import { PageTitle, Notice, useFiltered, useTimer } from '../../components/shared';
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
    <div className="audio-player">
      <div className="audio-main">
        <button className="primary audio-play" onClick={() => play(sentences)}>
          <SkillIcon skill="play" size={20} />
          {t('listen')}
        </button>
        <button onClick={stopSpeech}>
          <SkillIcon skill="stop" size={16} />
          {t('stop')}
        </button>
        <div
          className="audio-speed"
          role="group"
          aria-label={bi('Tốc độ bài nghe', 'Playback speed')}
        >
          {[0.75, 1, 1.25].map((n) => (
            <button key={n} type="button" aria-pressed={speed === n} onClick={() => setSpeed(n)}>
              {n}×
            </button>
          ))}
        </div>
      </div>
      {sentences.length > 1 && (
        <div className="audio-lines">
          <p className="muted">
            {bi('Nghe lại từng câu', 'Replay a sentence')} · {settings.accent}
          </p>
          <div className="audio-line-buttons">
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
        </div>
      )}
      {error && <Notice error>{error}</Notice>}
    </div>
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
      <PageTitle title={lesson.title} meta={`${lesson.level} · ${lesson.topic}`} />
      <div className="split">
        <div className="session-stack">
          <section className="panel" aria-labelledby="listening-audio">
            <h2 id="listening-audio">{bi('Bài nghe', 'Audio')}</h2>
            <AudioPlayer lines={lesson.lines} reveal={submitted || settings.transcript} />
          </section>
          {submitted || settings.transcript ? (
            <section className="panel">
              <h2>{bi('Bản chép lời', 'Transcript')}</h2>
              {lesson.lines.map((line, i) => (
                <div className="transcript-line" key={i}>
                  <strong>{line.speaker}</strong>
                  <DictionaryText text={line.text} />
                </div>
              ))}
            </section>
          ) : (
            <p className="panel locked-note">
              <SkillIcon skill="lock" size={20} />
              {bi(
                'Bản chép lời sẽ mở sau khi bạn trả lời.',
                'The transcript unlocks after you answer.',
              )}
            </p>
          )}
        </div>
        <section className="panel">
          <Questions
            questions={lesson.questions}
            answers={answers}
            submitted={submitted}
            onChange={(id, v) => setAnswers({ ...answers, [id]: v })}
            checking={busy}
            onCheck={() => {
              setBusy(true);
              void logAttempt('listening', score, start, lesson.title)
                .then(() => setSubmitted(true))
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
        meta={`${item.level} · ${item.topic}`}
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
  const allLessons = byLevel(listenings);
  const allSentences = byLevel(dictations);
  const lessons = useFiltered(allLessons);
  const sentences = useFiltered(allSentences);
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
      <PageTitle title={t('listening')} />
      <div className="tabs">
        <button aria-pressed={tab === 'lessons'} onClick={() => setTab('lessons')}>
          {bi('Hội thoại & bài nói', 'Dialogues & talks')}
        </button>
        <button aria-pressed={tab === 'dictation'} onClick={() => setTab('dictation')}>
          {bi('Chép chính tả', 'Dictation')}
        </button>
      </div>
      {tab === 'lessons' ? (
        <LessonBrowser
          skill="listening"
          all={allLessons}
          onOpen={setActive}
          describe={(l) => ({
            meta: `${l.lines.length} ${bi('lượt nói', 'speaking turns')} · ${l.questions.length} ${bi('câu hỏi', 'questions')}`,
          })}
        />
      ) : (
        <LessonBrowser
          skill="listening"
          all={allSentences.map((d, i) => ({ ...d, title: `${bi('Câu', 'Sentence')} ${i + 1}` }))}
          onOpen={(d) => setDictation(dictations.find((x) => x.id === d.id))}
          keyOf={(d) => `Dictation ${d.id}`}
          describe={(d) => ({ meta: `${d.text.split(/\s+/).length} ${bi('từ', 'words')}` })}
        />
      )}
    </>
  );
}
