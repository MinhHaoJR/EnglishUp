import { useCallback, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useBi, useT } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import { ApiError, useAuth } from '../../services/auth';
import { syncNow } from '../../services/sync';
import {
  answerQuestion,
  fetchRecords,
  finishGame,
  startGame,
  type GameRecords,
  type GameResult,
  type GameStart,
} from '../../services/game';

const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const;
// Long enough to see which option was right, short enough to keep the race moving.
const FEEDBACK_MS = 450;

type Play = {
  game: GameStart;
  index: number;
  score: number;
  combo: number;
  endsAt: number;
  feedback: { choice: number; answer: number } | null;
};

export default function Game() {
  const bi = useBi();
  const t = useT();
  const email = useAuth((state) => state.email);
  const [level, setLevel] = useState('all');
  const [records, setRecords] = useState<GameRecords | null>(null);
  const [play, setPlay] = useState<Play | null>(null);
  const [result, setResult] = useState<GameResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);
  const [now, setNow] = useState(() => Date.now());
  const finishing = useRef(false);
  const playing = play !== null;

  useEffect(() => {
    if (!email || playing) return;
    let current = true;
    fetchRecords()
      .then((loaded) => current && setRecords(loaded))
      .catch(() => current && setRecords(null));
    return () => {
      current = false;
    };
  }, [email, playing, result]);

  const finish = useCallback(async (id: string) => {
    if (finishing.current) return;
    finishing.current = true;
    try {
      setResult(await finishGame(id));
      // Refreshes points and badges shown elsewhere.
      void syncNow();
    } catch {
      setFailed(true);
    } finally {
      setPlay(null);
      finishing.current = false;
    }
  }, []);

  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(() => setNow(Date.now()), 200);
    return () => clearInterval(timer);
  }, [playing]);

  useEffect(() => {
    if (play && now >= play.endsAt) void finish(play.game.id);
  }, [now, play, finish]);

  async function begin() {
    setBusy(true);
    setFailed(false);
    setResult(null);
    try {
      const game = await startGame(level === 'all' ? null : level);
      const start = Date.now();
      setNow(start);
      setPlay({
        game,
        index: 0,
        score: 0,
        combo: 0,
        endsAt: start + game.durationSeconds * 1000,
        feedback: null,
      });
    } catch {
      setFailed(true);
    } finally {
      setBusy(false);
    }
  }

  async function choose(choice: number) {
    if (!play || busy || play.feedback) return;
    setBusy(true);
    try {
      const reply = await answerQuestion(play.game.id, play.index, choice);
      setPlay({
        ...play,
        score: reply.score,
        combo: reply.combo,
        feedback: { choice, answer: reply.answer },
      });
      const next = play.index + 1;
      setTimeout(() => {
        if (next >= play.game.questions.length) void finish(play.game.id);
        else
          setPlay((current) =>
            current?.game.id === play.game.id
              ? { ...current, index: next, feedback: null }
              : current,
          );
      }, FEEDBACK_MS);
    } catch (error) {
      if (error instanceof ApiError && error.status === 409) void finish(play.game.id);
      else setFailed(true);
    } finally {
      setBusy(false);
    }
  }

  const title = (
    <PageTitle
      title={bi('Đua 60 giây', '60-second race')}
      description={bi(
        'Chọn nghĩa đúng cho càng nhiều từ càng tốt trong 60 giây.',
        'Pick the right meaning for as many words as you can in 60 seconds.',
      )}
    />
  );

  if (!email)
    return (
      <>
        {title}
        <Notice>
          {bi('Trò chơi được chấm trên máy chủ. Hãy', 'Games are graded on the server. Please')}{' '}
          <Link to="/account">
            {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
          </Link>{' '}
          {bi('để chơi.', 'to play.')}
        </Notice>
      </>
    );

  const error = failed && (
    <Notice error>
      {bi(
        'Không kết nối được máy chủ trò chơi. Hãy kiểm tra mạng rồi thử lại.',
        'Cannot reach the game server. Check your connection and try again.',
      )}
    </Notice>
  );

  if (play) {
    const question = play.game.questions[play.index];
    const secondsLeft = Math.max(0, Math.ceil((play.endsAt - now) / 1000));
    return (
      <>
        {title}
        <div className="stats">
          <div className="stat">
            <span>{bi('Thời gian', 'Time left')}</span>
            <strong>{secondsLeft}s</strong>
            <progress
              value={secondsLeft}
              max={play.game.durationSeconds}
              aria-label={bi('Thời gian còn lại', 'Time left')}
            />
          </div>
          <div className="stat">
            <span>{bi('Điểm ván', 'Score')}</span>
            <strong>{play.score}</strong>
          </div>
          <div className="stat">
            <span>Combo</span>
            <strong>×{play.combo}</strong>
          </div>
        </div>
        <section className="panel flashcard">
          <p className="muted">
            {bi('Câu', 'Question')} {play.index + 1}
          </p>
          <h2 lang="en">{question.word}</h2>
          <div className="choice-grid">
            {question.options.map((option, i) => {
              const feedback = play.feedback;
              const mark = !feedback
                ? ''
                : i === feedback.answer
                  ? 'right'
                  : i === feedback.choice
                    ? 'wrong'
                    : '';
              return (
                <button
                  key={`${play.index}-${i}`}
                  className={mark}
                  disabled={busy || feedback !== null}
                  onClick={() => void choose(i)}
                >
                  {option}
                  {mark === 'right' && ' ✓'}
                  {mark === 'wrong' && ' ✗'}
                </button>
              );
            })}
          </div>
          <p role="status" aria-live="polite">
            {play.feedback &&
              (play.feedback.choice === play.feedback.answer
                ? bi('Đúng!', 'Correct!')
                : `${bi('Chưa đúng. Đáp án', 'Not quite. Answer')}: ${question.options[play.feedback.answer]}`)}
          </p>
        </section>
        {error}
      </>
    );
  }

  return (
    <>
      {title}
      {result && (
        <section className="panel space-y-4" aria-labelledby="game-result">
          <h2 id="game-result">
            {result.isRecord ? bi('Kỷ lục mới!', 'New record!') : bi('Hết giờ!', "Time's up!")}
          </h2>
          <div className="stats">
            <div className="stat">
              <span>{bi('Điểm ván', 'Score')}</span>
              <strong>{result.score}</strong>
            </div>
            <div className="stat">
              <span>{bi('Trả lời đúng', 'Correct')}</span>
              <strong>
                {result.correct}
                <small> / {result.answered}</small>
              </strong>
            </div>
            <div className="stat">
              <span>{bi('Combo cao nhất', 'Best combo')}</span>
              <strong>×{result.maxCombo}</strong>
            </div>
            <div className="stat">
              <span>{bi('Điểm tích luỹ nhận được', 'Points earned')}</span>
              <strong>+{result.pointsEarned}</strong>
            </div>
          </div>
          <p className="muted">
            {bi('Kỷ lục của bạn', 'Your best')}: {result.best}
          </p>
        </section>
      )}
      <section className="panel space-y-4">
        <label>
          {t('level')}
          <select value={level} onChange={(e) => setLevel(e.target.value)}>
            <option value="all">{t('allLevels')}</option>
            {levels.map((value) => (
              <option key={value}>{value}</option>
            ))}
          </select>
        </label>
        {records && (
          <p>
            {bi('Kỷ lục', 'Best score')}: <strong>{records.best}</strong> ·{' '}
            {bi('Số ván đã chơi', 'Games played')}: {records.played}
          </p>
        )}
        <p className="muted">
          {bi(
            'Điểm ván = 10 × câu đúng + 5 × combo cao nhất. Điểm tích luỹ = điểm ván / 10, dùng chung giới hạn điểm mỗi ngày.',
            'Score = 10 × correct + 5 × best combo. Points earned = score / 10, sharing the daily points cap.',
          )}
        </p>
        <div className="actions">
          <button className="primary" disabled={busy} onClick={() => void begin()}>
            {result ? bi('Chơi lại', 'Play again') : bi('Bắt đầu', 'Start')}
          </button>
        </div>
      </section>
      {error}
    </>
  );
}
