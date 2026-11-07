import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createElement } from 'react';
import Account from '../features/account/Account';
import { AuthError, authFetch, login, logout, register, restoreSession, useAuth } from './auth';

const json = (status: number, body?: unknown) =>
  new Response(body === undefined ? null : JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
const tokens = (accessToken = 'access-1', expiresIn = 3600) => ({
  tokenType: 'Bearer',
  accessToken,
  refreshToken: `refresh-${accessToken}`,
  expiresIn,
});
const kind = (promise: Promise<unknown>) =>
  promise.then(
    () => 'ok',
    (e: unknown) => (e instanceof AuthError ? e.kind : 'other'),
  );

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  localStorage.clear();
  logout();
  fetchMock = vi.fn();
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

describe('auth service', () => {
  it('stores the session outside Dexie and sends the bearer token', async () => {
    fetchMock.mockResolvedValueOnce(json(200, tokens())).mockResolvedValueOnce(json(200, {}));
    await login(' learner@example.test ', 'Learn#2026');
    expect(useAuth.getState().email).toBe('learner@example.test');
    expect(localStorage.getItem('englishup.session')).toContain('access-1');
    await authFetch('/api/manage/info');
    const headers = fetchMock.mock.calls[1][1].headers as Headers;
    expect(headers.get('Authorization')).toBe('Bearer access-1');
  });

  it('maps login and registration failures', async () => {
    fetchMock.mockResolvedValueOnce(json(401, { detail: 'Failed' }));
    expect(await kind(login('a@example.test', 'x'))).toBe('invalid');
    fetchMock.mockResolvedValueOnce(json(401, { detail: 'LockedOut' }));
    expect(await kind(login('a@example.test', 'x'))).toBe('locked');
    fetchMock.mockResolvedValueOnce(json(400, { errors: { DuplicateUserName: ['taken'] } }));
    expect(await kind(register('a@example.test', 'Learn#2026'))).toBe('exists');
    fetchMock.mockResolvedValueOnce(json(400, { errors: { PasswordRequiresUpper: ['x'] } }));
    expect(await kind(register('a@example.test', 'learn#2026'))).toBe('password');
    fetchMock.mockRejectedValueOnce(new TypeError('offline'));
    expect(await kind(login('a@example.test', 'x'))).toBe('network');
    expect(useAuth.getState().email).toBeNull();
  });

  it('registers and signs in with the same credentials', async () => {
    fetchMock.mockResolvedValueOnce(json(200)).mockResolvedValueOnce(json(200, tokens()));
    await register('new@example.test', 'Learn#2026');
    expect(fetchMock.mock.calls.map((call) => call[0])).toEqual(['/api/register', '/api/login']);
    expect(useAuth.getState().email).toBe('new@example.test');
  });

  it('refreshes an expiring token before calling the API', async () => {
    fetchMock
      .mockResolvedValueOnce(json(200, tokens('old', 10)))
      .mockResolvedValueOnce(json(200, tokens('new')))
      .mockResolvedValueOnce(json(200, {}));
    await login('a@example.test', 'Learn#2026');
    await authFetch('/api/manage/info');
    expect(fetchMock.mock.calls[1][0]).toBe('/api/refresh');
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({ refreshToken: 'refresh-old' });
    expect((fetchMock.mock.calls[2][1].headers as Headers).get('Authorization')).toBe('Bearer new');
  });

  it('signs out when the server rejects the session, but keeps it while offline', async () => {
    fetchMock.mockResolvedValueOnce(json(200, tokens()));
    await login('a@example.test', 'Learn#2026');
    fetchMock.mockRejectedValueOnce(new TypeError('offline'));
    await restoreSession();
    expect(useAuth.getState().email).toBe('a@example.test');
    fetchMock.mockResolvedValueOnce(json(401));
    await restoreSession();
    expect(useAuth.getState().email).toBeNull();
    expect(localStorage.getItem('englishup.session')).toBeNull();
  });
});

describe('account page', () => {
  it('signs in, shows the account and signs out', async () => {
    const user = userEvent.setup();
    fetchMock.mockResolvedValueOnce(json(401, { detail: 'Failed' }));
    render(createElement(Account));
    await user.type(screen.getByLabelText('Email'), 'learner@example.test');
    await user.type(screen.getByLabelText('Mật khẩu'), 'Wrong#2026');
    // [0] is the mode tab; [1] submits the form.
    await user.click(screen.getAllByRole('button', { name: 'Đăng nhập' })[1]);
    expect(await screen.findByRole('alert')).toHaveTextContent('Email hoặc mật khẩu không đúng.');

    fetchMock.mockResolvedValueOnce(json(200, tokens()));
    await user.click(screen.getAllByRole('button', { name: 'Đăng nhập' })[1]);
    expect(await screen.findByText('learner@example.test')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Đăng xuất' }));
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
  });

  it('shows the password policy when registration is rejected', async () => {
    const user = userEvent.setup();
    fetchMock.mockResolvedValueOnce(json(400, { errors: { PasswordRequiresDigit: ['x'] } }));
    render(createElement(Account));
    await user.click(screen.getByRole('button', { name: 'Đăng ký' }));
    await user.type(screen.getByLabelText('Email'), 'learner@example.test');
    await user.type(screen.getByLabelText('Mật khẩu'), 'NoDigits#Here');
    await user.click(screen.getByRole('button', { name: 'Tạo tài khoản' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('ít nhất 8 ký tự');
    expect(useAuth.getState().email).toBeNull();
  });
});
