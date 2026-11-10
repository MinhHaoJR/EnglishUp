import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Account from '../features/account/Account';
import Achievements from '../features/achievements/Achievements';
import { useAuth } from '../services/auth';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const board = (period: string, myRowShown = true) => ({
  period,
  entries: [
    { rank: 1, displayName: 'Lan', points: 120, isMe: false },
    { rank: 2, displayName: 'Minh', points: 45, isMe: myRowShown },
  ],
  myPoints: 45,
  myRowShown,
});

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

const show = (element: React.ReactElement) => render(<MemoryRouter>{element}</MemoryRouter>);

describe('Achievements page', () => {
  it('asks signed-out learners to sign in', () => {
    useAuth.setState({ email: null });
    show(<Achievements />);
    expect(screen.getByRole('link', { name: 'đăng nhập hoặc tạo tài khoản' })).toHaveAttribute(
      'href',
      '/login?next=/achievements',
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('shows earned and locked badges and switches leaderboard periods', async () => {
    fetchMock.mockImplementation((path: string) =>
      Promise.resolve(
        path === '/api/achievements'
          ? json([
              { code: 'first-practice', points: 10, earnedAt: '2026-11-08T10:00:00Z' },
              { code: 'streak-7', points: 50 },
            ])
          : json(board(path.endsWith('all') ? 'all' : 'week')),
      ),
    );
    show(<Achievements />);

    const badges = await screen.findByRole('list', { name: 'Huy hiệu' });
    expect(within(badges).getByText('Bước đầu tiên').closest('li')).not.toHaveClass('locked');
    expect(within(badges).getByText('Một tuần bền bỉ').closest('li')).toHaveClass('locked');
    expect(within(badges).getByText('Chưa đạt · +50 điểm')).toBeInTheDocument();

    const rows = screen.getAllByRole('listitem').filter((row) => row.closest('[role="list"]'));
    expect(rows[1]).toHaveAttribute('aria-current', 'true');
    expect(screen.getByText('Minh (bạn)')).toBeInTheDocument();

    await userEvent.click(screen.getByRole('button', { name: 'Mọi thời gian' }));
    await waitFor(() =>
      expect(fetchMock.mock.calls.map(([path]) => path)).toContain('/api/leaderboard?period=all'),
    );
  });

  it('tells hidden learners how to appear and reports load failures', async () => {
    fetchMock.mockImplementation((path: string) =>
      Promise.resolve(path === '/api/achievements' ? json([]) : json(board('week', false))),
    );
    const { unmount } = show(<Achievements />);
    expect(await screen.findByText(/Bạn có 45 điểm nhưng đang ẩn/)).toBeInTheDocument();
    unmount();

    fetchMock.mockReset();
    fetchMock.mockRejectedValue(new TypeError('offline'));
    show(<Achievements />);
    expect(await screen.findByText(/Không tải được thành tích/)).toBeInTheDocument();
  });
});

describe('Account profile form', () => {
  it('saves a trimmed display name and the leaderboard choice', async () => {
    fetchMock.mockImplementation((path: string, init?: RequestInit) =>
      Promise.resolve(
        path === '/api/profile' && init?.method === 'PUT'
          ? json(JSON.parse(init.body as string))
          : path === '/api/profile'
            ? json({ displayName: 'Học viên 1234', showOnLeaderboard: false })
            : json({}),
      ),
    );
    show(<Account />);

    const name = await screen.findByRole('textbox', { name: 'Tên hiển thị' });
    await userEvent.clear(name);
    await userEvent.type(name, '  Minh Hào ');
    await userEvent.click(screen.getByRole('checkbox', { name: /Hiện tôi trên bảng xếp hạng/ }));
    await userEvent.click(screen.getByRole('button', { name: 'Lưu hồ sơ' }));

    expect(await screen.findByText('Đã lưu hồ sơ.')).toBeInTheDocument();
    const put = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === 'PUT');
    expect(JSON.parse((put![1] as RequestInit).body as string)).toEqual({
      displayName: 'Minh Hào',
      showOnLeaderboard: true,
    });
  });

  it('previews the leaderboard row live, without the email', async () => {
    fetchMock.mockImplementation((path: string) =>
      Promise.resolve(
        path === '/api/profile'
          ? json({ displayName: 'Học viên 1234', showOnLeaderboard: true })
          : json({}, 500),
      ),
    );
    show(<Account />);
    const name = await screen.findByRole('textbox', { name: 'Tên hiển thị' });
    const preview = screen.getByRole('figure');
    expect(within(preview).getByText('Học viên 1234')).toBeInTheDocument();
    await userEvent.clear(name);
    await userEvent.type(name, 'Minh');
    expect(within(preview).getByText('Minh')).toBeInTheDocument();
    expect(within(preview).queryByText(/learner@example.test/)).not.toBeInTheDocument();
    await userEvent.click(screen.getByRole('checkbox', { name: /Hiện tôi trên bảng xếp hạng/ }));
    expect(within(preview).getByText('Bạn đang ẩn khỏi bảng xếp hạng.')).toBeInTheDocument();
  });

  it('explains a rejected save', async () => {
    fetchMock.mockImplementation((path: string, init?: RequestInit) =>
      Promise.resolve(
        init?.method === 'PUT'
          ? json({ errors: { displayName: ['bad'] } }, 400)
          : path === '/api/profile'
            ? json({ displayName: 'Học viên 1234', showOnLeaderboard: false })
            : json({}),
      ),
    );
    show(<Account />);
    await screen.findByRole('textbox', { name: 'Tên hiển thị' });
    await userEvent.click(screen.getByRole('button', { name: 'Lưu hồ sơ' }));
    expect(await screen.findByText(/Không lưu được/)).toBeInTheDocument();
  });
});
