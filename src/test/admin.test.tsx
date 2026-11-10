import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Admin from '../features/admin/Admin';
import { useAuth } from '../services/auth';
import { startPresence, useAdmin } from '../services/admin';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const now = new Date().toISOString();
const overview = {
  users: 3,
  online: 1,
  offline: 2,
  activeToday: 2,
  locked: 0,
  admins: 1,
  attemptsToday: 12,
  questionsToday: 3,
  gamesToday: 1,
  knowledgeChunks: 2102,
  onlineWindowSeconds: 120,
  at: now,
};
const users = [
  {
    id: 'a',
    email: 'admin@example.test',
    displayName: 'Admin',
    showOnLeaderboard: false,
    isAdmin: true,
    locked: false,
    lastSeenAt: now,
    online: true,
    points: 5,
    attempts: 2,
  },
  {
    id: 'b',
    email: 'lan@example.test',
    displayName: 'Lan',
    showOnLeaderboard: true,
    isAdmin: false,
    locked: false,
    lastSeenAt: '2020-01-01T00:00:00Z',
    online: false,
    points: 40,
    attempts: 9,
  },
  {
    id: 'c',
    email: 'new@example.test',
    showOnLeaderboard: false,
    isAdmin: false,
    locked: false,
    online: false,
    points: 0,
    attempts: 0,
  },
];

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  localStorage.setItem(
    'englishup.session',
    JSON.stringify({
      email: 'admin@example.test',
      accessToken: 'a',
      refreshToken: 'r',
      expiresAt: Date.now() + 3_600_000,
    }),
  );
  useAuth.setState({ email: 'admin@example.test' });
  useAdmin.setState({ isAdmin: true });
  fetchMock = vi.fn((path: string) =>
    Promise.resolve(
      path === '/api/admin/overview'
        ? json(overview)
        : path.startsWith('/api/admin/users?') || path === '/api/admin/users'
          ? json(users)
          : new Response(null, { status: 204 }),
    ),
  );
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
  useAdmin.setState({ isAdmin: false });
});

const show = () =>
  render(
    <MemoryRouter>
      <Admin />
    </MemoryRouter>,
  );

test('non-admins see a refusal and no data is requested', () => {
  useAdmin.setState({ isAdmin: false });
  show();
  expect(screen.getByText(/chỉ dành cho quản trị viên/)).toBeInTheDocument();
  expect(fetchMock).not.toHaveBeenCalled();
});

test('shows the online split and puts users on the time spine', async () => {
  show();
  expect(await screen.findByText('đang online')).toBeInTheDocument();
  expect(screen.getByRole('img', { name: '1 trên 3 tài khoản đang online' })).toBeInTheDocument();
  const online = screen.getByRole('region', { name: 'Đang online' });
  expect(within(online).getByText('admin@example.test')).toBeInTheDocument();
  expect(
    within(screen.getByRole('region', { name: 'Lâu hơn' })).getByText('lan@example.test'),
  ).toBeInTheDocument();
  expect(
    within(screen.getByRole('region', { name: 'Chưa mở app từ khi có theo dõi' })).getByText(
      'new@example.test',
    ),
  ).toBeInTheDocument();
  // Admins cannot lock themselves.
  expect(within(online).queryByRole('button', { name: 'Khoá tài khoản' })).not.toBeInTheDocument();
});

test('locking asks for confirmation, then calls the API', async () => {
  show();
  const row = (await screen.findByText('lan@example.test')).closest('li')!;
  await userEvent.click(within(row).getByRole('button', { name: 'Khoá tài khoản' }));
  expect(fetchMock.mock.calls.some(([p]) => String(p).includes('/lock'))).toBe(false);
  await userEvent.click(within(row).getByRole('button', { name: 'Xác nhận khoá' }));
  const call = fetchMock.mock.calls.find(([p]) => p === '/api/admin/users/b/lock');
  expect(JSON.parse((call![1] as RequestInit).body as string)).toEqual({ locked: true });
});

test('search filters on the server', async () => {
  show();
  await screen.findByText('lan@example.test');
  await userEvent.type(screen.getByRole('searchbox', { name: 'Tìm người dùng' }), 'lan');
  await vi.waitFor(() =>
    expect(fetchMock.mock.calls.some(([p]) => p === '/api/admin/users?search=lan')).toBe(true),
  );
});

test('presence heartbeats only while signed in', async () => {
  vi.useFakeTimers();
  const presence = () => fetchMock.mock.calls.filter(([p]) => p === '/api/presence').length;
  const stop = startPresence(1000);
  expect(presence()).toBe(1);
  await vi.advanceTimersByTimeAsync(1000);
  expect(presence()).toBe(2);
  useAuth.setState({ email: null });
  await vi.advanceTimersByTimeAsync(3000);
  expect(presence()).toBe(2);
  stop();
  vi.useRealTimers();
});
