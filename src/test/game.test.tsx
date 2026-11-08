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
function serve(options: { durationSeconds?: number; answerStatus?: number } = {}) {
  fetchMock.mockImplementation((path: string, init?: RequestInit) => {
    if (path === '/api/game/records') return Promise.resolve(json({ best: 0, played: 0 }));
    if (path === '/api/game/start') return Promise.resolve(json(start(options.durationSeconds)));
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
  expect(JSON.parse((startCall![1] as RequestInit).body as string)).toEqual({ level: 'B1' });

  await userEvent.click(screen.getByRole('button', { name: 'thói quen' }));
  expect(await screen.findByText('Đúng!')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'thói quen ✓' })).toBeDisabled();

  expect(await screen.findByRole('heading', { name: 'harbour' })).toBeInTheDocument();
  await userEvent.click(screen.getByRole('button', { name: 'ngọn núi' }));
  expect(await screen.findByText('Chưa đúng. Đáp án: bến cảng')).toBeInTheDocument();
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
