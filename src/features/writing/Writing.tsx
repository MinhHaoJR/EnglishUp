import { useEffect, useRef, useState } from 'react';
import { writingPrompts } from '../../data/content';
import type { WritingPrompt } from '../../data/schema';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import {
  Filters,
  PageTitle,
  Notice,
  Empty,
  useFiltered,
  useLive,
  useTimer,
} from '../../components/shared';
import { WordDiff } from '../../components/WordDiff';
import { db, type Submission } from '../../services/storage';
import { feedbackProvider, countWords, type Feedback } from '../../services/feedback';
function WritingSession({ prompt, onBack }: { prompt: WritingPrompt; onBack: () => void }) {
  const t = useT();
  const bi = useBi();
  const language = useApp((s) => s.settings.language);
  const [text, setText] = useState('');
  const [ready, setReady] = useState(false);
  const [saving, setSaving] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState<Feedback>();
  const [submittedText, setSubmittedText] = useState<string>();
  const [checks, setChecks] = useState<boolean[]>(prompt.checklist.map(() => false));
  const [compare, setCompare] = useState('');
  const latest = useRef('');
  const attemptStart = useRef(Date.now());
  const { seconds } = useTimer(!feedback || text !== submittedText);
  const { value: history = [] } = useLive(
    () => db.submissions.where('promptId').equals(prompt.id).reverse().sortBy('timestamp'),
    [prompt.id],
  );
  useEffect(() => {
    let active = true;
    void db.drafts
      .get(prompt.id)
      .then((draft) => {
        if (active) {
          latest.current = draft?.text ?? '';
          setText(latest.current);
          setReady(true);
        }
      })
      .catch(() => {
        if (active) setError(t('error'));
      });
    return () => {
      active = false;
    }; // Reload only when the prompt changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prompt.id]);
  function change(value: string) {
    setText(value);
    latest.current = value;
    setSaving(true);
    void db.drafts
      .put({ id: prompt.id, text: value, updated: Date.now() })
      .then(() => {
        if (latest.current === value) setSaving(false);
      })
      .catch(() => setError(t('error')));
  }
  async function submit() {
    setBusy(true);
    setError('');
    try {
      const report = await feedbackProvider.evaluate(text, prompt, language);
      const now = Date.now();
      const submission: Submission = {
        id: crypto.randomUUID(),
        promptId: prompt.id,
        text,
        timestamp: now,
        score: report.score,
        feedback: report.notes,
      };
      await db.transaction('rw', db.submissions, db.attempts, db.drafts, async () => {
        await db.submissions.add(submission);
        await db.drafts.put({ id: prompt.id, text, updated: now });
        await db.attempts.add({
          id: crypto.randomUUID(),
          skill: 'writing',
          score: report.score,
          duration: Math.max(1, Math.round((now - attemptStart.current) / 1000)),
          timestamp: now,
          label: prompt.title,
        });
      });
      setFeedback(report);
      setSubmittedText(text);
      attemptStart.current = now;
    } catch {
      setError(t('error'));
    } finally {
      setBusy(false);
    }
  }
  const previous = history.find((s) => s.id === compare);
  return (
    <>
      <button className="mb-5" onClick={onBack}>
        ← {t('back')}
      </button>
      <PageTitle
        eyebrow={`${prompt.level} · ${prompt.topic} · ${prompt.genre}`}
        title={prompt.title}
      />
      <div className="split">
        <section className="panel">
          <p className="writing-prompt">{prompt.prompt}</p>
          <div className="editor-toolbar">
            <span>
              {countWords(text)} / {prompt.minWords}–{prompt.maxWords} {t('words')}
            </span>
            <span>
              {Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, '0')} ·{' '}
              {saving ? bi('Đang lưu…', 'Saving…') : ready ? t('saved') : t('loading')}
            </span>
          </div>
          <label className="sr-only" htmlFor="writing-editor">
            {t('draft')}
          </label>
          <textarea
            id="writing-editor"
            className="writing-editor"
            disabled={!ready || busy}
            maxLength={15000}
            spellCheck
            lang="en"
            value={text}
            onChange={(e) => change(e.target.value)}
            placeholder={bi('Bắt đầu với một ý tưởng…', 'Start with one idea…')}
          />
          <div className="actions mt-5">
            <button
              className="primary"
              disabled={!ready || busy || !text.trim() || text === submittedText}
              onClick={() => void submit()}
            >
              {busy ? t('loading') : bi('Nhận phản hồi & lưu bài', 'Get feedback & save')}
            </button>
          </div>
          {error && <Notice error>{error}</Notice>}
        </section>
        <section className="panel">
          <h2>{bi('Trước khi nộp bài', 'Before you submit')}</h2>
          {prompt.checklist.map((c, i) => (
            <label className="checkbox mt-5" key={c}>
              <input
                type="checkbox"
                checked={checks[i]}
                onChange={(e) => setChecks(checks.map((v, n) => (n === i ? e.target.checked : v)))}
              />
              {c}
            </label>
          ))}
          <div className="notice mt-6">
            <strong>
              {bi('Nhận xét theo quy tắc · Không cần mạng', 'Rule-based feedback · Offline')}
            </strong>
            <p>
              {bi(
                'Tự kiểm tra nội dung theo đề. Hệ thống hỗ trợ về độ dài, từ nối, từ lặp, dấu câu và một số lỗi thường gặp.',
                'Check the meaning against the prompt yourself. The provider checks length, linking, repetition, punctuation and common error patterns.',
              )}
            </p>
          </div>
        </section>
      </div>
      {feedback && (
        <section className="panel" aria-label={t('feedback')}>
          <h2>
            {t('feedback')} · {feedback.score}/100{' '}
            <span className="badge">{bi('Điểm quy tắc', 'Rule score')}</span>
          </h2>
          <div className="metrics-grid">
            {Object.entries(feedback.scores).map(([name, score]) => (
              <div key={name}>
                <strong>{score}</strong>
                <span>
                  {
                    (
                      {
                        task: bi('Độ dài', 'Length'),
                        coherence: bi('Liên kết', 'Coherence'),
                        vocabulary: bi('Từ vựng', 'Vocabulary'),
                        grammar: bi('Quy tắc ngữ pháp', 'Grammar rules'),
                      } as Record<string, string>
                    )[name]
                  }
                </span>
              </div>
            ))}
          </div>
          <ul className="list-disc pl-5 space-y-3">
            {feedback.notes.map((n) => (
              <li key={n}>{n}</li>
            ))}
          </ul>
          <Notice>{t('result')}</Notice>
        </section>
      )}
      <section className="panel">
        <h2>{t('history')}</h2>
        {!history.length ? (
          <p className="muted">
            {bi(
              'Bài đã nộp sẽ xuất hiện ở đây. Bản nháp luôn được lưu riêng.',
              'Submitted work will appear here. Your draft is saved separately.',
            )}
          </p>
        ) : (
          <>
            <label>
              {t('compare')}
              <select value={compare} onChange={(e) => setCompare(e.target.value)}>
                <option value="">
                  {bi(
                    'Chọn bài cũ để so với bản nháp hiện tại',
                    'Choose an earlier submission to compare with your draft',
                  )}
                </option>
                {history.map((s) => (
                  <option key={s.id} value={s.id}>
                    {new Date(s.timestamp).toLocaleString(language)} · {s.score}%
                  </option>
                ))}
              </select>
            </label>
            {previous && (
              <div className="mt-5">
                <div className="form-grid">
                  <div>
                    <h3>{bi('Bài đã nộp', 'Earlier submission')}</h3>
                    <p className="prose">{previous.text}</p>
                  </div>
                  <div>
                    <h3>{t('draft')}</h3>
                    <p className="prose">{text}</p>
                  </div>
                </div>
                <p className="muted mt-4">
                  {bi(
                    'So sánh văn bản: chỉ báo thay đổi, không phải điểm chất lượng.',
                    'Text comparison: indicates edits, not writing quality.',
                  )}
                </p>
                <WordDiff target={previous.text} actual={text} />
              </div>
            )}
            {history.map((s) => (
              <details key={s.id} className="history-item">
                <summary>
                  {new Date(s.timestamp).toLocaleString(language)} · {s.score}/100 ·{' '}
                  {countWords(s.text)} {t('words')}
                </summary>
                <p className="prose my-4">{s.text}</p>
                <ul className="list-disc pl-5 space-y-2">
                  {s.feedback.map((n, i) => (
                    <li key={i}>{n}</li>
                  ))}
                </ul>
              </details>
            ))}
          </>
        )}
      </section>
    </>
  );
}
export default function Writing() {
  const t = useT();
  const bi = useBi();
  const prompts = useFiltered(writingPrompts);
  const [active, setActive] = useState<WritingPrompt>();
  if (active)
    return <WritingSession key={active.id} prompt={active} onBack={() => setActive(undefined)} />;
  return (
    <>
      <PageTitle
        eyebrow={bi('DIỄN ĐẠT Ý TƯỞNG CỦA BẠN', 'MAKE YOUR IDEAS HEARD')}
        title={t('writing')}
        description={bi(
          'Từ một ý tưởng nhỏ đến một bài viết rõ ràng.',
          'Turn a small idea into clear writing.',
        )}
      />
      <Filters />
      {prompts.length ? (
        <div className="lesson-grid">
          {prompts.map((p) => (
            <article className="panel lesson-card" key={p.id}>
              <span className="badge">
                {p.level} · {p.topic} · {p.genre}
              </span>
              <h2>{p.title}</h2>
              <p className="muted">{p.prompt}</p>
              <span className="muted">
                {p.minWords}–{p.maxWords} {t('words')}
              </span>
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
