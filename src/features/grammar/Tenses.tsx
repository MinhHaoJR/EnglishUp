import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useBi } from '../../i18n';
import { LevelTopic, Notice } from '../../components/shared';
import { SpeakButton } from '../../components/SpeakButton';
import SkillIcon from '../../components/SkillIcon';
import { tenses } from '../../data/content';
import type { Tense } from '../../data/schema';
import { logAttempt } from '../../services/storage';

/** The three times, in reading order, each with its own colour on the timeline. */
const times: { id: Tense['group']; vi: string; en: string }[] = [
  { id: 'past', vi: 'Quá khứ', en: 'Past' },
  { id: 'present', vi: 'Hiện tại', en: 'Present' },
  { id: 'future', vi: 'Tương lai', en: 'Future' },
];

/** Every English tense: a timeline to pick one, then its form, uses, signal words, a tip and a quick check. */
export default function Tenses() {
  const bi = useBi();
  const [params, setParams] = useSearchParams();
  const ordered = [...tenses].sort((a, b) => a.order - b.order);
  const current = ordered.find((t) => t.id === params.get('tense')) ?? ordered[0];
  if (!current)
    return <Notice>{bi('Chưa có nội dung về các thì.', 'There is no tense content yet.')}</Notice>;

  const pick = (id: string) =>
    setParams((previous) => {
      const next = new URLSearchParams(previous);
      next.set('part', 'tenses');
      next.set('tense', id);
      return next;
    });

  return (
    <div className="tenses">
      <nav className="tense-timeline" aria-label={bi('Chọn thì', 'Choose a tense')}>
        {times.map((time) => (
          <section key={time.id} className="tense-time" data-time={time.id}>
            <h2>{bi(time.vi, time.en)}</h2>
            <ul>
              {ordered
                .filter((t) => t.group === time.id)
                .map((t) => (
                  <li key={t.id}>
                    <button
                      type="button"
                      aria-current={t.id === current.id ? 'true' : undefined}
                      onClick={() => pick(t.id)}
                    >
                      <span>{bi(t.name.vi, t.name.en)}</span>
                      <small lang="en">{t.name.en}</small>
                    </button>
                  </li>
                ))}
            </ul>
          </section>
        ))}
      </nav>
      <TenseCard key={current.id} tense={current} />
    </div>
  );
}

const formRows = [
  { key: 'affirmative', sign: '+', vi: 'Khẳng định', en: 'Affirmative' },
  { key: 'negative', sign: '−', vi: 'Phủ định', en: 'Negative' },
  { key: 'question', sign: '?', vi: 'Nghi vấn', en: 'Question' },
] as const;

function TenseCard({ tense }: { tense: Tense }) {
  const bi = useBi();
  return (
    <article className="panel tense-card" data-time={tense.group} aria-labelledby="tense-title">
      <header>
        <LevelTopic level={tense.level} topic={bi(...timeName(tense.group))} />
        <h2 id="tense-title">{bi(tense.name.vi, tense.name.en)}</h2>
        <p className="muted" lang="en">
          {tense.name.en}
        </p>
      </header>

      <section aria-labelledby="tense-form">
        <h3 id="tense-form">{bi('Công thức', 'Form')}</h3>
        <dl className="tense-forms">
          {formRows.map((row) => (
            <div key={row.key}>
              <dt>
                <span className="tense-sign" aria-hidden="true">
                  {row.sign}
                </span>
                {bi(row.vi, row.en)}
              </dt>
              <dd lang="en">
                {tense.forms[row.key].map((form) => (
                  <code key={form}>{form}</code>
                ))}
              </dd>
            </div>
          ))}
        </dl>
      </section>

      <section aria-labelledby="tense-uses">
        <h3 id="tense-uses">{bi('Cách dùng', 'Uses')}</h3>
        <ol className="tense-uses">
          {tense.uses.map((use) => (
            <li key={use.example}>
              <strong>{bi(use.vi, use.en)}</strong>
              <span className="tense-example">
                <span lang="en">{use.example}</span>
                <SpeakButton text={use.example} />
              </span>
            </li>
          ))}
        </ol>
      </section>

      <section aria-labelledby="tense-signals">
        <h3 id="tense-signals">{bi('Dấu hiệu nhận biết', 'Signal words')}</h3>
        <ul className="tense-signals">
          {tense.signals.map((signal) => (
            <li key={signal} lang="en">
              {signal}
            </li>
          ))}
        </ul>
      </section>

      <p className="tense-tip">
        <SkillIcon skill="goal" size={18} />
        <span>
          <strong>{bi('Lưu ý', 'Tip')}:</strong> {bi(tense.tip.vi, tense.tip.en)}
        </span>
      </p>

      <QuickCheck tense={tense} />
    </article>
  );
}

const timeName = (group: Tense['group']): [string, string] => {
  const time = times.find((t) => t.id === group)!;
  return [time.vi, time.en];
};

/** Three fill-in-the-blank checks; the score is saved to the practice log once all are answered. */
function QuickCheck({ tense }: { tense: Tense }) {
  const bi = useBi();
  const [started] = useState(Date.now);
  const [answers, setAnswers] = useState<(string | null)[]>(() => tense.practice.map(() => null));
  const [saved, setSaved] = useState<'idle' | 'saved' | 'failed'>('idle');
  const right = tense.practice.filter((q, i) => answers[i] === q.answer).length;
  const finished = answers.every((a) => a !== null);

  async function choose(index: number, option: string) {
    if (answers[index] !== null) return;
    const next = answers.map((a, i) => (i === index ? option : a));
    setAnswers(next);
    if (next.every((a) => a !== null)) {
      const score = Math.round(
        (tense.practice.filter((q, i) => next[i] === q.answer).length / tense.practice.length) *
          100,
      );
      try {
        await logAttempt('grammar', score, started, `Các thì / Tenses · ${tense.name.en}`);
        setSaved('saved');
      } catch {
        setSaved('failed');
      }
    }
  }

  return (
    <section className="tense-check" aria-labelledby="tense-check">
      <h3 id="tense-check">{bi('Luyện nhanh', 'Quick check')}</h3>
      <ol>
        {tense.practice.map((q, i) => {
          const [before, after] = q.sentence.split('___');
          const answer = answers[i];
          return (
            <li key={q.sentence}>
              <p className="tense-sentence" lang="en">
                {before}
                <span className={answer ? 'game-blank filled' : 'game-blank'}>
                  {answer ? q.answer : <span className="sr-only">___</span>}
                </span>
                {after}
              </p>
              <div className="choice-grid">
                {q.options.map((option) => {
                  const mark = !answer
                    ? ''
                    : option === q.answer
                      ? 'right'
                      : option === answer
                        ? 'wrong'
                        : '';
                  return (
                    <button
                      key={option}
                      lang="en"
                      className={mark}
                      disabled={answer !== null}
                      onClick={() => void choose(i, option)}
                    >
                      {option}
                      {mark === 'right' && ' ✓'}
                      {mark === 'wrong' && ' ✗'}
                    </button>
                  );
                })}
              </div>
              {answer && (
                <p
                  className={answer === q.answer ? 'tense-feedback ok' : 'tense-feedback'}
                  role="status"
                >
                  {answer === q.answer ? bi('Đúng!', 'Correct!') : bi('Chưa đúng.', 'Not quite.')}{' '}
                  {q.explanation}
                </p>
              )}
            </li>
          );
        })}
      </ol>
      {finished && (
        <p className="tense-score">
          {bi(
            `Kết quả: ${right}/${tense.practice.length} câu đúng.`,
            `Result: ${right} of ${tense.practice.length} right.`,
          )}{' '}
          {saved === 'saved' && bi('Đã lưu vào nhật ký luyện tập.', 'Saved to your practice log.')}
          {saved === 'failed' && bi('Không lưu được kết quả.', 'Could not save the result.')}
        </p>
      )}
    </section>
  );
}
