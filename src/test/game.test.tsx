import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Game from '../features/game/Game';
import { useAuth } from '../services/auth';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const gameId = '0b9c7a52-8d7b-4c1e-9a65-7f3c2a1e5d40';
const start = (durationSeconds = 60) => ({
  id: gameId,
  durationSeconds,
  questions: [
    { word: 'routine', options: ['thói quen', 'quả táo', 'con mèo', 'bầu trời'] },
    { word: 'harbour', options: ['bến cảng', 'ngọn núi', 'cái bàn', 'dòng sông'] },
  ],
});
const grammar = {
  id: gameId,
  durationSeconds: 60,
  questions: [
    { word: 'They ___ football now.', options: ['are playing', 'play', 'plays', 'is playing'] },
  ],
};
const board = (path: string) => ({
  mode: path.includes('grammar') ? 'grammar' : 'vocabulary',
  period: path.includes('all') ? 'all' : 'week',
  entries: [
    { rank: 1, displayName: 'An', best: 180, played: 3, isMe: false },
    { rank: 2, displayName: 'Bạn học', best: 120, played: 5, isMe: true },
  ],
  myBest: 120,
  myRowShown: true,
});
const result = {
  score: 15,
  correct: 1,
  answered: 2,
  maxCombo: 1,
  pointsEarned: 1,
  best: 15,
  isRecord: true,
};

/** A fake game server where option 0 is right for every question. */
function serve(
  options: { durationSeconds?: number; answerStatus?: number; game?: typeof grammar } = {},
) {
  fetchMock.mockImplementation((path: string, init?: RequestInit) => {
    if (path.startsWith('/api/game/records')) return Promise.resolve(json({ best: 0, played: 0 }));
    if (path.startsWith('/api/game/leaderboard')) return Promise.resolve(json(board(path)));
    if (path === '/api/game/start')
      return Promise.resolve(json(options.game ?? start(options.durationSeconds)));
    if (path.endsWith('/answer')) {
      if (options.answerStatus) return Promise.resolve(json({}, options.answerStatus));
      const { index, choice } = JSON.parse(init!.body as string) as {
        index: number;
        choice: number;
      };
      return Promise.resolve(
        json({
          correct: choice === 0,
          answer: 0,
          combo: choice === 0 ? 1 : 0,
          score: index * 10 + 10,
          ...(options.game && { explanation: 'Có now → hiện tại tiếp diễn.' }),
        }),
      );
    }
    if (path.endsWith('/finish')) return Promise.resolve(json(result));
    if (path === '/api/sync') return Promise.resolve(json({ attempts: [], records: [] }));
    return Promise.resolve(json({ total: 1, today: 1, dailyCap: 300 }));
  });
}
const called = (suffix: string) =>
  fetchMock.mock.calls.some(([path]) => String(path).endsWith(suffix));

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  localStorage.setItem(
    'englishup.session',
    JSON.stringify({
      email: 'learner@example.test',
      accessToken: 'access',
      refreshToken: 'refresh',
      expiresAt: Date.now() + 3_600_000,
    }),
  );
  useAuth.setState({ email: 'learner@example.test' });
  fetchMock = vi.fn();
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
});

const show = () =>
  render(
    <MemoryRouter>
      <Game />
    </MemoryRouter>,
  );

it('asks signed-out learners to sign in before playing', () => {
  useAuth.setState({ email: null });
  show();
  expect(screen.getByRole('link', { name: 'đăng nhập hoặc tạo tài khoản' })).toBeInTheDocument();
  expect(fetchMock).not.toHaveBeenCalled();
});

it('plays through the questions with server feedback and shows the result', async () => {
  serve();
  show();
  await userEvent.selectOptions(screen.getByRole('combobox', { name: 'Trình độ' }), 'B1');
  await userEvent.click(screen.getByRole('button', { name: 'Bắt đầu' }));

  expect(await screen.findByRole('heading', { name: 'routine' })).toBeInTheDocument();
  const startCall = fetchMock.mock.calls.find(([path]) => path === '/api/game/start');
  expect(JSON.parse((startCall![1] as RequestInit).body as string)).toEqual({
    level: 'B1',
    mode: 'vocabulary',
    category: null,
  });

  await userEvent.click(screen.getByRole('button', { name: 'thói quen' }));
  expect(await screen.findByText('Đúng!')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'thói quen ✓' })).toBeDisabled();

  expect(await screen.findByRole('heading', { name: 'harbour' })).toBeInTheDocument();
  await userEvent.click(screen.getByRole('button', { name: 'ngọn núi' }));
  expect(
    await screen.findByText(
      (_, el) => el?.tagName === 'P' && el.textContent === 'Chưa đúng. Đáp án: bến cảng',
    ),
  ).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'ngọn núi ✗' })).toBeInTheDocument();

  expect(await screen.findByRole('heading', { name: 'Kỷ lục mới!' })).toBeInTheDocument();
  expect(screen.getByText('+1')).toBeInTheDocument();
  await waitFor(() => expect(called('/api/sync')).toBe(true));
  expect(screen.getByRole('button', { name: 'Chơi lại' })).toBeInTheDocument();
});

it('finishes when the timer runs out', async () => {
  serve({ durationSeconds: 1 });
  show();
  await userEvent.click(screen.getByRole('button', { name: 'Bắt đầu' }));
  expect(await screen.findByRole('heading', { name: 'routine' })).toBeInTheDocument();

  expect(
    await screen.findByRole('heading', { name: 'Kỷ lục mới!' }, { timeout: 3000 }),
  ).toBeInTheDocument();
  expect(called('/finish')).toBe(true);
});

it('finishes when the server says time is up', async () => {
  serve({ answerStatus: 409 });
  show();
  await userEvent.click(screen.getByRole('button', { name: 'Bắt đầu' }));
  await userEvent.click(await screen.findByRole('button', { name: 'thói quen' }));
  expect(await screen.findByRole('heading', { name: 'Kỷ lục mới!' })).toBeInTheDocument();
});

it('plays the grammar race: a sentence with a blank, then why the answer is right', async () => {
  serve({ game: grammar });
  show();
  await userEvent.click(screen.getByRole('tab', { name: /Đua ngữ pháp/ }));
  await userEvent.selectOptions(screen.getByRole('combobox', { name: 'Dạng ngữ pháp' }), 'tense');
  await userEvent.click(screen.getByRole('button', { name: 'Bắt đầu' }));

  const startCall = fetchMock.mock.calls.find(([path]) => path === '/api/game/start');
  expect(JSON.parse((startCall![1] as RequestInit).body as string)).toEqual({
    level: null,
    mode: 'grammar',
    category: 'tense',
  });
  expect(
    await screen.findByRole('heading', { name: /They\s+___\s+football now\./ }),
  ).toBeInTheDocument();
  await userEvent.click(screen.getByRole('button', { name: 'play' }));
  expect(await screen.findByText('Có now → hiện tại tiếp diễn.')).toBeInTheDocument();
  // The blank now shows the right answer.
  expect(
    screen.getByRole('heading', { name: /They are playing football now\./ }),
  ).toBeInTheDocument();
});

it('ranks players by their best game, this week or ever, per race', async () => {
  serve();
  show();
  const ranks = await screen.findAllByRole('listitem');
  expect(ranks.map((li) => li.textContent)).toEqual([
    expect.stringContaining('An'),
    expect.stringContaining('Bạn học (bạn)'),
  ]);
  expect(ranks[1]).toHaveAttribute('aria-current');
  await userEvent.click(screen.getByRole('button', { name: 'Mọi thời gian' }));
  await userEvent.click(screen.getByRole('tab', { name: /Đua ngữ pháp/ }));
  expect(
    await screen.findByRole('heading', { name: 'Bảng xếp hạng Đua ngữ pháp' }),
  ).toBeInTheDocument();
  expect(called('/api/game/leaderboard?mode=grammar&period=all')).toBe(true);
});
