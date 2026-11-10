import { useCallback, useEffect, useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useBi, useT } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { quizCategories, type QuizCategory } from '../../data/schema';
import { ApiError, useAuth } from '../../services/auth';
import { syncNow } from '../../services/sync';
import {
  answerQuestion,
  fetchGameLeaderboard,
  fetchRecords,
  finishGame,
  startGame,
  type GameLeaderboard,
  type GameMode,
  type GamePeriod,
  type GameRecords,
  type GameResult,
  type GameStart,
} from '../../services/game';

const levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const;
// Long enough to see which option was right, short enough to keep the race moving.
const FEEDBACK_MS = 450;
// A wrong grammar answer shows why; that needs a moment to read.
const EXPLAIN_MS = 2200;

type Play = {
  game: GameStart;
  mode: GameMode;
  index: number;
  score: number;
  combo: number;
  endsAt: number;
  feedback: { choice: number; answer: number; explanation?: string } | null;
};

const modes: {
  id: GameMode;
  skill: string;
  icon: 'vocabulary' | 'grammar';
  vi: string;
  en: string;
}[] = [
  { id: 'vocabulary', skill: 'vocabulary', icon: 'vocabulary', vi: 'Từ vựng', en: 'Vocabulary' },
  { id: 'grammar', skill: 'grammar', icon: 'grammar', vi: 'Ngữ pháp', en: 'Grammar' },
];

/** The sentence with its blank drawn as a box; after an answer the box holds the right option. */
function Sentence({ text, filled }: { text: string; filled?: string }) {
  const [before, after] = text.split('___');
  return (
    <h2 lang="en" className="game-sentence">
      {before}
      <span className={filled ? 'game-blank filled' : 'game-blank'}>
        {filled ?? <span className="sr-only">___</span>}
      </span>
      {after}
    </h2>
  );
}

export default function Game() {
  const bi = useBi();
  const t = useT();
  const email = useAuth((state) => state.email);
  const [params, setParams] = useSearchParams();
  const mode: GameMode = params.get('mode') === 'grammar' ? 'grammar' : 'vocabulary';
  // A learning-path task can open a race at a level and grammar point (?level=B1&category=tense).
  const [level, setLevel] = useState(() => {
    const requested = params.get('level');
    return requested && (levels as readonly string[]).includes(requested) ? requested : 'all';
  });
  const [category, setCategory] = useState(() => {
    const requested = params.get('category');
    return requested && requested in quizCategories ? requested : 'all';
  });
  const [records, setRecords] = useState<GameRecords | null>(null);
  const [play, setPlay] = useState<Play | null>(null);
  const [result, setResult] = useState<GameResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState<'network' | 'empty' | null>(null);
  const [now, setNow] = useState(() => Date.now());
  const finishing = useRef(false);
  const playing = play !== null;

  useEffect(() => {
    if (!email || playing) return;
    let current = true;
    fetchRecords(mode)
      .then((loaded) => current && setRecords(loaded))
      .catch(() => current && setRecords(null));
    return () => {
      current = false;
    };
  }, [email, playing, result, mode]);

  const finish = useCallback(async (id: string) => {
    if (finishing.current) return;
    finishing.current = true;
    try {
      setResult(await finishGame(id));
      // Refreshes points and badges shown elsewhere.
      void syncNow();
    } catch {
      setFailed('network');
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
    setFailed(null);
    setResult(null);
    try {
      const game = await startGame(
        level === 'all' ? null : level,
        mode,
        mode === 'grammar' && category !== 'all' ? category : null,
      );
      const start = Date.now();
      setNow(start);
      setPlay({
        game,
        mode,
        index: 0,
        score: 0,
        combo: 0,
        endsAt: start + game.durationSeconds * 1000,
        feedback: null,
      });
    } catch (error) {
      // 400: no question matches this level and grammar point.
      setFailed(error instanceof ApiError && error.status === 400 ? 'empty' : 'network');
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
        feedback: { choice, answer: reply.answer, explanation: reply.explanation },
      });
      const next = play.index + 1;
      const wait = play.mode === 'grammar' && !reply.correct ? EXPLAIN_MS : FEEDBACK_MS;
      setTimeout(() => {
        if (next >= play.game.questions.length) void finish(play.game.id);
        else
          setPlay((current) =>
            current?.game.id === play.game.id
              ? { ...current, index: next, feedback: null }
              : current,
          );
      }, wait);
    } catch (error) {
      if (error instanceof ApiError && error.status === 409) void finish(play.game.id);
      else setFailed('network');
    } finally {
      setBusy(false);
    }
  }

  const title = (
    <PageTitle
      title={bi('Trò chơi', 'Games')}
      description={bi(
        'Đua 60 giây: chọn nghĩa đúng của từ, hoặc chọn từ đúng điền vào chỗ trống trong câu.',
        '60-second races: pick the meaning of a word, or the word that fills the blank in a sentence.',
      )}
    />
  );

  if (!email)
    return (
      <>
        {title}
        <Notice>
          {bi('Trò chơi được chấm trên máy chủ. Hãy', 'Games are graded on the server. Please')}{' '}
          <Link to="/login?next=/game">
            {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
          </Link>{' '}
          {bi('để chơi.', 'to play.')}
        </Notice>
      </>
    );

  const error =
    failed === 'empty' ? (
      <Notice error>
        {bi(
          'Chưa có câu hỏi cho trình độ và dạng ngữ pháp này. Hãy chọn trình độ hoặc dạng khác.',
          'There are no questions for this level and grammar point yet. Choose another level or point.',
        )}
      </Notice>
    ) : failed === 'network' ? (
      <Notice error>
        {bi(
          'Không kết nối được máy chủ trò chơi. Hãy kiểm tra mạng rồi thử lại.',
          'Cannot reach the game server. Check your connection and try again.',
        )}
      </Notice>
    ) : null;

  if (play) {
    const question = play.game.questions[play.index];
    const secondsLeft = Math.max(0, Math.ceil((play.endsAt - now) / 1000));
    const feedback = play.feedback;
    return (
      <div data-skill={play.mode}>
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
            {play.mode === 'grammar' &&
              ` · ${bi('Chọn từ thích hợp điền vào chỗ trống', 'Choose the word that fills the blank')}`}
          </p>
          {play.mode === 'grammar' ? (
            <Sentence
              text={question.word}
              filled={feedback ? question.options[feedback.answer] : undefined}
            />
          ) : (
            <h2 lang="en">{question.word}</h2>
          )}
          <div className="choice-grid">
            {question.options.map((option, i) => {
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
                  lang={play.mode === 'grammar' ? 'en' : undefined}
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
          <div role="status" aria-live="polite" className="game-feedback">
            {feedback &&
              (feedback.choice === feedback.answer ? (
                <p>{bi('Đúng!', 'Correct!')}</p>
              ) : (
                <>
                  <p>
                    {bi('Chưa đúng. Đáp án', 'Not quite. Answer')}:{' '}
                    <strong lang="en">{question.options[feedback.answer]}</strong>
                  </p>
                  {feedback.explanation && <p className="muted">{feedback.explanation}</p>}
                </>
              ))}
          </div>
        </section>
        {error}
      </div>
    );
  }

  const current = modes.find((m) => m.id === mode)!;
  return (
    <>
      {title}
      <div className="game-modes" role="tablist" aria-label={bi('Chọn trò chơi', 'Choose a game')}>
        {modes.map((m) => (
          <button
            key={m.id}
            type="button"
            role="tab"
            aria-selected={m.id === mode}
            data-skill={m.skill}
            onClick={() => {
              setParams(m.id === 'grammar' ? { mode: 'grammar' } : {});
              setResult(null);
              setFailed(null);
            }}
          >
            <span className="line-tile" aria-hidden="true">
              <SkillIcon skill={m.icon} size={20} />
            </span>
            <span>
              <strong>{bi(`Đua ${m.vi.toLowerCase()}`, `${m.en} race`)}</strong>
              <small>
                {m.id === 'grammar'
                  ? bi(
                      'Điền từ đúng vào chỗ trống: thì, mạo từ, giới từ, trạng từ, cấu trúc câu…',
                      'Fill the blank: tenses, articles, prepositions, adverbs, sentence patterns…',
                    )
                  : bi(
                      'Chọn nghĩa tiếng Việt đúng của từ.',
                      'Pick the Vietnamese meaning of a word.',
                    )}
              </small>
            </span>
          </button>
        ))}
      </div>

      {result && (
        <section
          className="panel space-y-4"
          aria-labelledby="game-result"
          data-skill={current.skill}
        >
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
      <section className="panel space-y-4" data-skill={current.skill}>
        <div className="game-options">
          <label>
            {t('level')}
            <select value={level} onChange={(e) => setLevel(e.target.value)}>
              <option value="all">{t('allLevels')}</option>
              {levels.map((value) => (
                <option key={value}>{value}</option>
              ))}
            </select>
          </label>
          {mode === 'grammar' && (
            <label>
              {bi('Dạng ngữ pháp', 'Grammar point')}
              <select value={category} onChange={(e) => setCategory(e.target.value)}>
                <option value="all">{bi('Mọi dạng', 'Every point')}</option>
                {(Object.keys(quizCategories) as QuizCategory[]).map((c) => (
                  <option key={c} value={c}>
                    {bi(quizCategories[c][0], quizCategories[c][1])}
                  </option>
                ))}
              </select>
            </label>
          )}
        </div>
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
      <GameBoard mode={mode} refresh={result} />
    </>
  );
}

/** The mode's leaderboard: each learner's best game this week or ever. */
function GameBoard({ mode, refresh }: { mode: GameMode; refresh: unknown }) {
  const bi = useBi();
  const [period, setPeriod] = useState<GamePeriod>('week');
  const [board, setBoard] = useState<GameLeaderboard | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let current = true;
    setFailed(false);
    fetchGameLeaderboard(mode, period)
      .then((loaded) => current && setBoard(loaded))
      .catch(() => current && setFailed(true));
    return () => {
      current = false;
    };
  }, [mode, period, refresh]);

  return (
    <section className="panel space-y-4 game-board" aria-labelledby="game-board-title">
      <h2 id="game-board-title">
        {mode === 'grammar'
          ? bi('Bảng xếp hạng Đua ngữ pháp', 'Grammar race leaderboard')
          : bi('Bảng xếp hạng Đua từ vựng', 'Vocabulary race leaderboard')}
      </h2>
      <p className="muted">
        {bi(
          'Xếp theo điểm ván cao nhất của mỗi người.',
          "Ranked by each player's best game score.",
        )}
      </p>
      <div className="tabs">
        {(['week', 'all'] as const).map((value) => (
          <button key={value} aria-pressed={period === value} onClick={() => setPeriod(value)}>
            {value === 'week' ? bi('Tuần này', 'This week') : bi('Mọi thời gian', 'All time')}
          </button>
        ))}
      </div>
      {failed && (
        <Notice error>
          {bi('Không tải được bảng xếp hạng.', 'Could not load the leaderboard.')}
        </Notice>
      )}
      {board && !board.myRowShown && (
        <Notice>
          {bi(
            `Kỷ lục của bạn là ${board.myBest} điểm nhưng bạn đang ẩn khỏi bảng xếp hạng. Bật hiển thị trong`,
            `Your best is ${board.myBest} but you are hidden from the leaderboard. Turn it on in`,
          )}{' '}
          <Link to="/account?tab=privacy">{bi('Tài khoản', 'Account')}</Link>.
        </Notice>
      )}
      {board &&
        (board.entries.length ? (
          <ol className="game-ranks">
            {board.entries.map((entry) => (
              <li key={entry.rank} aria-current={entry.isMe || undefined}>
                <span className={`game-rank r${Math.min(entry.rank, 4)}`}>{entry.rank}</span>
                <strong>
                  {entry.displayName}
                  {entry.isMe && ` (${bi('bạn', 'you')})`}
                </strong>
                <span className="muted">{bi(`${entry.played} ván`, `${entry.played} games`)}</span>
                <span className="game-best">
                  {entry.best} {bi('điểm', 'pts')}
                </span>
              </li>
            ))}
          </ol>
        ) : (
          <p className="muted">
            {period === 'week'
              ? bi(
                  'Tuần này chưa có ai chơi. Hãy là người đầu tiên!',
                  'Nobody has played this week yet. Be the first!',
                )
              : bi('Chưa có ai trên bảng xếp hạng.', 'Nobody is on the leaderboard yet.')}
          </p>
        ))}
    </section>
  );
}
