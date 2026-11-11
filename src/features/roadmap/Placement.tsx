import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useBi } from '../../i18n';
import { PageTitle } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { logAttempt } from '../../services/storage';
import {
  buildPlacement,
  LEVELS,
  PASS_SHARE,
  PER_LEVEL,
  roadmapFor,
  scorePlacement,
  type PlacementQuestion,
  type PlacementResult,
} from '../../services/placement';

type Test = { questions: PlacementQuestion[]; answers: number[]; started: number };

/** A thirty-question level test from A1 to C2; the score and the estimated level lead to a learning path. */
export default function Placement() {
  const bi = useBi();
  const { settings, update } = useApp();
  const [test, setTest] = useState<Test | null>(null);
  const [result, setResult] = useState<PlacementResult | null>(null);
  const [saving, setSaving] = useState(false);

  const title = (
    <PageTitle
      title={bi('Kiểm tra trình độ', 'Level test')}
      description={bi(
        'Chưa biết mình đang ở đâu? Làm 30 câu ngữ pháp và từ vựng từ A1 đến C2 để biết trình độ và lộ trình nên học.',
        'Not sure where you stand? Answer 30 grammar and vocabulary questions from A1 to C2 to find your level and the path to follow.',
      )}
    />
  );

  async function answer(choice: number) {
    if (!test) return;
    const answers = [...test.answers, choice];
    if (answers.length < test.questions.length) {
      setTest({ ...test, answers });
      return;
    }
    const scored = scorePlacement(test.questions, answers);
    setResult(scored);
    setTest(null);
    setSaving(true);
    try {
      await logAttempt(
        'grammar',
        scored.score,
        test.started,
        `Kiểm tra trình độ / Level test: ${scored.level ?? '< A1'}`,
      );
      await update({ placement: { level: scored.level, score: scored.score, at: Date.now() } });
    } finally {
      setSaving(false);
    }
  }

  if (test) {
    const index = test.answers.length;
    const question = test.questions[index];
    const [before, after] = question.prompt.split('___');
    return (
      <>
        {title}
        <section className="panel placement-question" aria-labelledby="placement-prompt">
          <div className="placement-progress">
            <span>
              {bi('Câu', 'Question')} {index + 1}/{test.questions.length}
            </span>
            <progress
              value={index}
              max={test.questions.length}
              aria-label={bi('Tiến độ bài kiểm tra', 'Test progress')}
            />
          </div>
          <p className="muted">
            {question.kind === 'grammar'
              ? bi('Chọn từ thích hợp điền vào chỗ trống.', 'Choose the word that fills the blank.')
              : bi('Chọn nghĩa đúng của từ.', 'Choose the meaning of the word.')}
          </p>
          <h2 id="placement-prompt" lang="en" className="game-sentence">
            {question.kind === 'grammar' ? (
              <>
                {before}
                <span className="game-blank">
                  <span className="sr-only">___</span>
                </span>
                {after}
              </>
            ) : (
              question.prompt
            )}
          </h2>
          <div className="choice-grid">
            {question.options.map((option, i) => (
              <button
                key={`${index}-${i}`}
                lang={question.kind === 'grammar' ? 'en' : undefined}
                onClick={() => void answer(i)}
              >
                <span className="option-key" aria-hidden="true">
                  {String.fromCharCode(65 + i)}
                </span>
                <span>{option}</span>
              </button>
            ))}
          </div>
          <div className="actions">
            <button type="button" onClick={() => void answer(-1)}>
              {bi('Bỏ qua câu này', 'Skip this question')}
            </button>
          </div>
        </section>
      </>
    );
  }

  const last = settings.placement;
  return (
    <>
      {title}
      {result && <Report result={result} saving={saving} />}
      <section className="panel placement-intro">
        <div className="placement-how">
          <h2>
            {result
              ? bi('Làm lại bài kiểm tra', 'Take the test again')
              : bi('Cách làm', 'How it works')}
          </h2>
          <ul className="placement-facts">
            <li>
              <SkillIcon skill="placement" size={18} />
              {bi(
                `30 câu, ${PER_LEVEL} câu mỗi trình độ từ A1 đến C2, dễ trước khó sau.`,
                `30 questions, ${PER_LEVEL} per level from A1 to C2, easiest first.`,
              )}
            </li>
            <li>
              <SkillIcon skill="grammar" size={18} />
              {bi(
                'Mỗi trình độ có câu điền ngữ pháp vào chỗ trống và câu chọn nghĩa từ vựng.',
                'Each level mixes fill-the-blank grammar and word-meaning questions.',
              )}
            </li>
            <li>
              <SkillIcon skill="goal" size={18} />
              {bi(
                `Điểm = số câu đúng / 30 × 100. Bạn đạt một trình độ khi đúng từ ${Math.ceil(PER_LEVEL * PASS_SHARE)}/${PER_LEVEL} câu của trình độ đó và mọi trình độ thấp hơn.`,
                `Score = right answers / 30 × 100. You reach a level with at least ${Math.ceil(PER_LEVEL * PASS_SHARE)}/${PER_LEVEL} right on it and on every level below.`,
              )}
            </li>
            <li>
              <SkillIcon skill="game" size={18} />
              {bi(
                'Không giới hạn thời gian. Không biết thì bấm "Bỏ qua", đừng đoán.',
                'No time limit. Skip rather than guess when you do not know.',
              )}
            </li>
          </ul>
        </div>
        <div className="placement-start">
          <p className="placement-length">
            {bi('30 câu · khoảng 10 phút', '30 questions · about 10 minutes')}
          </p>
          {last && !result && (
            <p className="muted">
              {bi('Lần trước', 'Last time')}: <strong>{last.score}/100</strong> ·{' '}
              {bi('trình độ', 'level')} {last.level ?? bi('dưới A1', 'below A1')} (
              {new Date(last.at).toLocaleDateString(settings.language === 'vi' ? 'vi-VN' : 'en-GB')}
              )
            </p>
          )}
          <button
            className="primary"
            onClick={() => {
              setResult(null);
              setTest({ questions: buildPlacement(), answers: [], started: Date.now() });
            }}
          >
            {result || last
              ? bi('Làm bài mới', 'Start a new test')
              : bi('Bắt đầu kiểm tra', 'Start the test')}
          </button>
        </div>
      </section>
    </>
  );
}

/** The score, the estimated level, how each level went and the path to follow next. */
function Report({ result, saving }: { result: PlacementResult; saving: boolean }) {
  const bi = useBi();
  const path = roadmapFor(result.level);
  const next = result.level === null ? 'A1' : LEVELS[Math.min(LEVELS.indexOf(result.level) + 1, 5)];
  return (
    <section className="panel space-y-4 placement-report" aria-labelledby="placement-result">
      <h2 id="placement-result">{bi('Kết quả của bạn', 'Your result')}</h2>
      <div className="placement-verdict">
        <div>
          <span>{bi('Điểm', 'Score')}</span>
          <strong>
            {result.score}
            <small>/100</small>
          </strong>
          <span className="muted">
            {bi(
              `${result.correct}/${result.total} câu đúng`,
              `${result.correct} of ${result.total} right`,
            )}
          </span>
        </div>
        <div data-skill="grammar">
          <span>{bi('Trình độ ước tính', 'Estimated level')}</span>
          <strong>{result.level ?? bi('Dưới A1', 'Below A1')}</strong>
          <span className="muted">
            {result.level === 'C2'
              ? bi('Trình độ cao nhất của bài', 'The top level of the test')
              : bi(`Mục tiêu tiếp theo: ${next}`, `Next goal: ${next}`)}
          </span>
        </div>
      </div>
      <ol className="placement-levels" aria-label={bi('Kết quả theo trình độ', 'Result by level')}>
        {result.perLevel.map((row) => (
          <li key={row.level} className={row.passed ? 'passed' : undefined}>
            <span className="placement-level">{row.level}</span>
            <span className="placement-bar" aria-hidden="true">
              <span style={{ width: `${row.total ? (row.correct / row.total) * 100 : 0}%` }} />
            </span>
            <span>
              {row.correct}/{row.total}
              {row.passed && <SkillIcon skill="check" size={16} />}
            </span>
          </li>
        ))}
      </ol>
      <p className="muted" role="status">
        {saving
          ? bi('Đang lưu kết quả…', 'Saving the result…')
          : bi(
              'Đã lưu vào nhật ký luyện tập (kỹ năng Cấu trúc câu) và hồ sơ học của bạn.',
              'Saved to your practice log (sentence patterns) and your learning profile.',
            )}
      </p>
      <div className="actions">
        <Link className="button primary" to={`/roadmap?path=${path}`}>
          <SkillIcon skill="roadmap" size={18} />
          {bi(
            `Xem lộ trình ${path.slice(3, 5).toUpperCase()} → ${path.slice(6).toUpperCase()}`,
            `Open the ${path.slice(3, 5).toUpperCase()} → ${path.slice(6).toUpperCase()} path`,
          )}
        </Link>
      </div>
    </section>
  );
}
