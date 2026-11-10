import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
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
  useAdmin.setState({ isAdmin: true, checkedFor: 'admin@example.test' });
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
  useAdmin.setState({ isAdmin: false, checkedFor: null });
});

const show = () =>
  render(
    <MemoryRouter initialEntries={['/admin']}>
      <Routes>
        <Route path="/admin" element={<Admin />} />
        <Route path="/" element={<p>Learning app</p>} />
        <Route path="/login" element={<p>Sign-in page</p>} />
      </Routes>
    </MemoryRouter>,
  );

test('a learner account is sent to the learning app and no admin data is requested', () => {
  useAdmin.setState({ isAdmin: false, checkedFor: 'admin@example.test' });
  show();
  expect(screen.getByText('Learning app')).toBeInTheDocument();
  expect(fetchMock.mock.calls.some(([p]) => String(p).startsWith('/api/admin'))).toBe(false);
});

test('signed out, the admin page asks for sign-in', () => {
  useAuth.setState({ email: null });
  show();
  expect(screen.getByText('Sign-in page')).toBeInTheDocument();
});

test('the admin page has its own header with a way back to learning', async () => {
  show();
  const header = screen.getAllByRole('banner')[0];
  expect(within(header).getByText('admin@example.test')).toBeInTheDocument();
  expect(within(header).getByRole('link', { name: 'Trang học tập' })).toHaveAttribute('href', '/');
  expect(within(header).getByRole('button', { name: 'Đăng xuất' })).toBeInTheDocument();
  await screen.findByText('đang online');
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
