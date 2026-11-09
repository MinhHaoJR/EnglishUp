import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import { useEffect, useState } from 'react';
import { speakingPrompts } from '../../data/content';
import type { SpeakingPrompt } from '../../data/schema';
import { useApp } from '../../app/store';
import SkillIcon from '../../components/SkillIcon';
import { useT, useBi } from '../../i18n';
import { Filters, PageTitle, Notice, Empty, useFiltered, useTimer } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
import { WordDiff } from '../../components/WordDiff';
import { alignWords } from '../../services/diff';
import { logAttempt } from '../../services/storage';
import { useRecorder } from '../../services/useRecorder';
import { speakingMetrics } from '../../services/speaking';
import { stopSpeech } from '../../services/speech';
function SpeakingSession({
  prompt,
  onBack,
  onContinue,
  hasNext,
}: {
  prompt: SpeakingPrompt;
  onBack: () => void;
  onContinue: () => void;
  hasNext: boolean;
}) {
  const t = useT();
  const bi = useBi();
  const settings = useApp((s) => s.settings);
  const rec = useRecorder(settings.accent);
  const [transcribe, setTranscribe] = useState(false);
  const [limit, setLimit] = useState(60);
  const [manual, setManual] = useState('');
  const [checks, setChecks] = useState<boolean[]>([false, false, false]);
  const [reviewed, setReviewed] = useState(false);
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const { start } = useTimer(!done);
  const text = rec.transcript || manual;
  const metrics = speakingMetrics(text, rec.duration);
  const automatic = prompt.mode === 'read' && !!rec.transcript;
  const score = automatic
    ? alignWords(prompt.text, rec.transcript).score
    : Math.round((checks.filter(Boolean).length / 3) * 100);
  useEffect(() => {
    if (rec.recording && rec.duration >= limit) rec.stop();
  }, [rec, limit]);
  const criteria =
    prompt.mode === 'read'
      ? [
          bi('Tôi nói đủ các từ trong câu.', 'I said all the words.'),
          bi('Tôi ngắt câu rõ ràng.', 'I used clear pauses.'),
          bi(
            'Tôi đã nghe lại và tìm điểm cần cải thiện.',
            'I listened back and found something to improve.',
          ),
        ]
      : [
          bi('Tôi trả lời đúng chủ đề.', 'I addressed the topic.'),
          bi('Tôi đưa ra ví dụ cụ thể.', 'I gave a specific example.'),
          bi('Các ý của tôi có liên kết.', 'I connected my ideas.'),
        ];
  return (
    <>
      <button className="mb-5" onClick={onBack}>
        ← {t('back')}
      </button>
      <PageTitle
        title={prompt.title}
        meta={`${prompt.level} · ${prompt.topic} · ${prompt.mode === 'read' ? bi('Đọc thành tiếng / nhại mẫu', 'Read aloud / shadowing') : bi('Nói theo chủ đề', 'Topic talk')}`}
      />
      <div className="split">
        <section className="panel">
          <p className="speaking-target">{prompt.text}</p>
          <ul className="list-disc pl-5 space-y-2 muted mb-5">
            {prompt.cues.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
          <SpeakButton text={prompt.text} />
          <p className="muted mt-4">
            {bi(
              'Nghe mẫu, sau đó ghi âm và thử bắt chước nhịp điệu. Điểm so khớp văn bản không phải điểm phát âm.',
              'Listen to the model, then record and imitate its rhythm. Text alignment is not a pronunciation score.',
            )}
          </p>
          <div className="notice">
            <p>
              {bi(
                'Bản ghi chỉ ở trong bộ nhớ phiên này. Nhận dạng giọng nói có thể gửi âm thanh đến dịch vụ của trình duyệt và cần internet.',
                'Recordings stay in this session’s memory. Browser speech recognition may send audio to a vendor service and require internet.',
              )}
            </p>
            <label className="checkbox mt-3">
              <input
                type="checkbox"
                disabled={!rec.recognitionSupported || rec.recording || done}
                checked={transcribe}
                onChange={(e) => setTranscribe(e.target.checked)}
              />
              {bi('Bật nhận dạng giọng nói của trình duyệt', 'Enable browser speech recognition')}
            </label>
          </div>
          {!rec.recognitionSupported && (
            <Notice>
              {bi(
                'Trình duyệt không hỗ trợ nhận dạng. Hãy ghi âm, nghe lại và tự đánh giá.',
                'Recognition is unsupported. Record, listen back and use self-assessment.',
              )}
            </Notice>
          )}
          {!rec.recordSupported && (
            <Notice>
              {bi(
                'Ghi âm không được hỗ trợ. Bạn vẫn có thể nói thành tiếng và tự đánh giá.',
                'Recording is unavailable. You can still speak aloud and self-assess.',
              )}
            </Notice>
          )}
          <label className="mt-5">
            {bi('Thời lượng tối đa', 'Time limit')}
            <select
              value={limit}
              disabled={rec.recording || done}
              onChange={(e) => setLimit(Number(e.target.value))}
            >
              <option value="60">60 s</option>
              <option value="90">90 s</option>
              <option value="120">120 s</option>
            </select>
          </label>
          <div className="record-controls">
            <strong className={rec.recording ? 'recording-dot' : ''}>
              {String(Math.floor(rec.duration / 60)).padStart(2, '0')}:
              {String(rec.duration % 60).padStart(2, '0')}
            </strong>
            {rec.recording ? (
              <button className="primary" onClick={rec.stop}>
                <SkillIcon skill="stop" size={16} />
                {t('stop')}
              </button>
            ) : (
              <button
                className="primary"
                disabled={done || rec.pending || !rec.recordSupported}
                onClick={() => {
                  stopSpeech();
                  setReviewed(false);
                  void rec.start(transcribe);
                }}
              >
                ●{' '}
                {rec.pending
                  ? t('loading')
                  : rec.audio
                    ? bi('Ghi âm lại', 'Record again')
                    : t('record')}
              </button>
            )}
          </div>
          {rec.error && (
            <Notice error>
              {rec.error === 'NotAllowedError'
                ? bi(
                    'Bạn chưa cho phép dùng micro. Bật quyền micro trong trình duyệt, hoặc tự đánh giá bên cạnh.',
                    'Microphone access was denied. Enable browser permission or use self-assessment.',
                  )
                : rec.error.startsWith('recognition')
                  ? bi(
                      'Nhận dạng chưa hoạt động. Bản ghi vẫn có thể dùng để tự đánh giá.',
                      'Recognition is unavailable. Your recording can still be used for self-assessment.',
                    )
                  : bi(
                      'Không mở được micro. Kiểm tra thiết bị và dùng HTTPS/localhost, hoặc tự đánh giá.',
                      'Could not open the microphone. Check the device and HTTPS/localhost, or self-assess.',
                    )}
            </Notice>
          )}
          {rec.audio && (
            <audio
              className="w-full mt-5"
              controls
              src={rec.audio}
              aria-label={bi('Bản ghi của bạn', 'Your recording')}
            />
          )}
        </section>
        <section className="panel">
          <h2>{bi('Nhìn lại phần nói của bạn', 'Reflect on your speaking')}</h2>
          <label>
            {rec.transcript
              ? bi('Văn bản nhận dạng (tự động)', 'Recognized transcript (automatic)')
              : bi(
                  'Ghi chú / bản chép lời thủ công (không bắt buộc)',
                  'Notes / manual transcript (optional)',
                )}
            <textarea
              maxLength={5000}
              disabled={rec.recording || done || !!rec.transcript}
              value={text}
              onChange={(e) => setManual(e.target.value)}
              placeholder={bi('Ghi lại những gì bạn đã nói…', 'Write down what you said…')}
            />
          </label>
          {prompt.mode === 'talk' && (
            <div className="metrics-grid">
              {[
                [t('words'), metrics.words],
                ['WPM', rec.duration ? metrics.wpm : '—'],
                [bi('Từ đệm', 'Fillers'), metrics.fillers],
                [bi('Độ đa dạng', 'Word variety'), `${metrics.variety}%`],
              ].map(([label, value]) => (
                <div key={label}>
                  <strong>{value}</strong>
                  <span>{label}</span>
                </div>
              ))}
            </div>
          )}
          {automatic && !rec.recording && <WordDiff target={prompt.text} actual={rec.transcript} />}
          <h3 className="mt-6">{t('selfAssess')}</h3>
          {criteria.map((c, i) => (
            <label className="checkbox mt-4" key={c}>
              <input
                type="checkbox"
                disabled={done}
                checked={checks[i]}
                onChange={(e) => setChecks(checks.map((v, n) => (n === i ? e.target.checked : v)))}
              />
              {c}
            </label>
          ))}
          <label className="checkbox mt-5">
            <input
              type="checkbox"
              disabled={done || rec.recording}
              checked={reviewed}
              onChange={(e) => setReviewed(e.target.checked)}
            />
            {bi(
              'Tôi đã thực hành nói và hoàn tất tự đánh giá.',
              'I practiced aloud and completed my self-assessment.',
            )}
          </label>
          {prompt.mode === 'talk' && rec.duration > 0 && rec.duration < 60 && (
            <p className="muted mt-3">
              {bi(
                'Thử nói ít nhất 60 giây trong lần tiếp theo.',
                'Try speaking for at least 60 seconds next time.',
              )}
            </p>
          )}
          {done ? (
            <Notice>
              {t('result')} · {score}% ·{' '}
              {automatic ? bi('So khớp văn bản', 'Text alignment') : t('selfAssess')}
            </Notice>
          ) : (
            <button
              className="primary mt-6"
              disabled={rec.recording || rec.pending || !reviewed || busy}
              onClick={() => {
                setBusy(true);
                void logAttempt(
                  'speaking',
                  score,
                  start,
                  `${prompt.title} (${automatic ? 'alignment' : 'self-assessed'})`,
                )
                  .then(() => setDone(true))
                  .catch(() => setError(t('error')))
                  .finally(() => setBusy(false));
              }}
            >
              {t('finish')}
            </button>
          )}
          {done && <LessonContinue onContinue={onContinue} hasNext={hasNext} />}
          {error && <Notice error>{error}</Notice>}
        </section>
      </div>
    </>
  );
}
export default function Speaking() {
  const t = useT();
  const bi = useBi();
  const prompts = useFiltered(speakingPrompts);
  const [mode, setMode] = useState('read');
  const [active, setActive] = useState<SpeakingPrompt>();
  const filtered = prompts.filter((p) => p.mode === mode);
  if (active)
    return (
      <SpeakingSession
        key={active.id}
        prompt={active}
        onBack={() => setActive(undefined)}
        onContinue={() => setActive(nextLesson(filtered, active))}
        hasNext={!!nextLesson(filtered, active)}
      />
    );
  return (
    <>
      <PageTitle title={t('speaking')} />
      <div className="tabs">
        <button aria-pressed={mode === 'read'} onClick={() => setMode('read')}>
          {bi('Đọc & nhại mẫu', 'Read & shadow')}
        </button>
        <button aria-pressed={mode === 'talk'} onClick={() => setMode('talk')}>
          {bi('Nói theo chủ đề', 'Topic talk')} · 60–120s
        </button>
      </div>
      <Filters />
      {filtered.length ? (
        <div className="lesson-grid">
          {filtered.map((p) => (
            <article className="panel lesson-card" key={p.id}>
              <span className="badge">
                {p.level} · {p.topic}
              </span>
              <h2>{p.title}</h2>
              <p className="muted">{p.text}</p>
              <button className="primary" onClick={() => setActive(p)}>
                {t('start')} →
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
