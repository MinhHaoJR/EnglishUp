import { useRef, useState } from 'react';
import type { Word } from '../../data/schema';
import { translations } from '../../data/content';
import { useBi, useT } from '../../i18n';
import { Empty, Notice, useFiltered } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
import { db } from '../../services/storage';
import {
  matchesTranslation,
  translationSession,
  translationSides,
  wordTranslation,
  type TranslationDirection,
  type TranslationItem,
} from '../../services/translation';

export default function TranslationPractice({ words }: { words: Word[] }) {
  const bi = useBi();
  const t = useT();
  const sentences = useFiltered(translations);
  const [kind, setKind] = useState<'word' | 'sentence'>('word');
  const [direction, setDirection] = useState<TranslationDirection>('vi-en');
  const [queue, setQueue] = useState<TranslationItem[]>([]);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [checked, setChecked] = useState(false);
  const [equivalent, setEquivalent] = useState(false);
  const [saved, setSaved] = useState(0);
  const [correct, setCorrect] = useState(0);
  const [error, setError] = useState(false);
  const [busy, setBusy] = useState(false);
  const saving = useRef(false);
  const started = useRef(0);
  const input = useRef<HTMLTextAreaElement>(null);
  const card = queue[index];
  const sides = card ? translationSides(card, direction) : undefined;
  const matched = sides ? matchesTranslation(answer, sides.answers) : false;
  const available = kind === 'word' ? words.map(wordTranslation) : sentences;

  async function save() {
    if (!card || !checked || saving.current) return;
    saving.current = true;
    setBusy(true);
    setError(false);
    try {
      const now = Date.now();
      const passed = matched || equivalent;
      await db.attempts.add({
        id: crypto.randomUUID(),
        skill: 'vocabulary',
        score: passed ? 100 : 0,
        duration: Math.max(1, Math.round((now - started.current) / 1000)),
        timestamp: now,
        label: `Translation ${direction}: ${card.en[0]}${equivalent && !matched ? ' (self-assessed)' : ''}`,
      });
      setSaved((n) => n + 1);
      setCorrect((n) => n + Number(passed));
      setIndex((n) => n + 1);
      setAnswer('');
      setChecked(false);
      setEquivalent(false);
      started.current = Date.now();
      input.current?.focus();
    } catch {
      setError(true);
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }

  return (
    <section
      className="panel space-y-4"
      aria-label={bi('Luyện viết và dịch', 'Translation practice')}
    >
      <h2>{bi('Luyện viết và dịch', 'Translation practice')}</h2>
      <p className="muted">
        {bi(
          'Viết bản dịch của bạn rồi đối chiếu đáp án. Luyện tự do, không giới hạn bởi lịch ôn; kết quả được lưu vào tiến độ từ vựng, không thay đổi lịch SRS.',
          'Write your translation, then compare answers. Free practice is independent of the review queue; results count towards vocabulary progress without changing SRS.',
        )}
      </p>
      {error && <Notice error>{t('error')}</Notice>}
      {card && sides ? (
        <>
          <p className="badge">
            {direction === 'vi-en' ? 'Tiếng Việt → English' : 'English → Tiếng Việt'} · {index + 1}{' '}
            / {queue.length}
          </p>
          <progress value={index} max={queue.length} aria-label={t('progress')} />
          <p className="text-xl" lang={direction === 'vi-en' ? 'vi' : 'en'}>
            {sides.prompt}
          </p>
          <form
            onSubmit={(event) => {
              event.preventDefault();
              if (answer.trim()) setChecked(true);
            }}
          >
            <label>
              {direction === 'vi-en'
                ? bi('Bản dịch tiếng Anh', 'English translation')
                : bi('Bản dịch tiếng Việt', 'Vietnamese translation')}
              <textarea
                ref={input}
                rows={3}
                maxLength={2000}
                lang={sides.language}
                value={answer}
                readOnly={checked}
                autoComplete="off"
                spellCheck={false}
                onChange={(event) => setAnswer(event.target.value)}
              />
            </label>
            {!checked && (
              <button className="primary mt-4" disabled={!answer.trim()}>
                {t('check')}
              </button>
            )}
          </form>
          {checked && (
            <div className="answer-box space-y-4">
              <Notice>
                {matched
                  ? bi('Khớp đáp án tham khảo!', 'Matches a reference answer!')
                  : bi(
                      'Chưa khớp đáp án tham khảo. Hãy đối chiếu cách dịch bên dưới.',
                      'Not a reference match. Compare your translation below.',
                    )}
              </Notice>
              <h3>{bi('Đáp án tham khảo', 'Reference answers')}</h3>
              <ul>
                {sides.answers.map((text) => (
                  <li key={text} lang={sides.language}>
                    {text}
                  </li>
                ))}
              </ul>
              <SpeakButton text={card.en[0]} />
              <p className="muted">
                {bi(
                  'So khớp bỏ qua chữ hoa, dấu câu và khoảng trắng, nhưng giữ dấu tiếng Việt. Đây không phải đánh giá ngữ nghĩa bằng AI; cách dịch khác vẫn có thể đúng.',
                  'Matching ignores case, punctuation and spacing, but preserves Vietnamese accents. This is not AI semantic grading; other translations may be correct.',
                )}
              </p>
              {!matched && (
                <label className="checkbox">
                  <input
                    type="checkbox"
                    checked={equivalent}
                    onChange={(event) => setEquivalent(event.target.checked)}
                  />
                  {bi(
                    'Tôi đã đối chiếu: bản dịch của tôi tương đương (tự đánh giá)',
                    'I compared the answers: my translation is equivalent (self-assessed)',
                  )}
                </label>
              )}
              <button className="primary" disabled={busy} onClick={() => void save()}>
                {bi('Lưu kết quả và tiếp tục', 'Save result and continue')}
              </button>
            </div>
          )}
          <button
            disabled={busy}
            onClick={() => {
              setQueue([]);
              setError(false);
            }}
          >
            {bi('Kết thúc (giữ kết quả đã lưu)', 'End session (keep saved results)')}
          </button>
        </>
      ) : (
        <>
          {queue.length > 0 && <h3>{t('result')}</h3>}
          {saved > 0 && (
            <Notice>
              {bi(
                `Đã lưu ${saved} lượt · ${correct}/${saved} khớp đáp án hoặc tự xác nhận.`,
                `Saved ${saved} attempts · ${correct}/${saved} matched or self-assessed as equivalent.`,
              )}
            </Notice>
          )}
          <div className="form-grid">
            <label>
              {bi('Nội dung luyện dịch', 'Translation content')}
              <select
                value={kind}
                onChange={(event) => setKind(event.target.value as 'word' | 'sentence')}
              >
                <option value="word">{bi('Dịch từ', 'Words')}</option>
                <option value="sentence">{bi('Dịch câu', 'Sentences')}</option>
              </select>
            </label>
            <label>
              {bi('Chiều dịch', 'Translation direction')}
              <select
                value={direction}
                onChange={(event) => setDirection(event.target.value as TranslationDirection)}
              >
                <option value="vi-en">Tiếng Việt → English</option>
                <option value="en-vi">English → Tiếng Việt</option>
              </select>
            </label>
          </div>
          <p>
            {bi(
              `${available.length} mục phù hợp bộ lọc · tối đa 10 mục ngẫu nhiên mỗi buổi.`,
              `${available.length} items match the filters · up to 10 random items per session.`,
            )}
          </p>
          <button
            className="primary"
            disabled={!available.length}
            onClick={() => {
              setQueue(translationSession(available));
              setIndex(0);
              setAnswer('');
              setChecked(false);
              setEquivalent(false);
              setSaved(0);
              setCorrect(0);
              setError(false);
              started.current = Date.now();
            }}
          >
            {bi('Bắt đầu luyện dịch', 'Start translating')}
          </button>
          {!available.length && <Empty />}
        </>
      )}
    </section>
  );
}
