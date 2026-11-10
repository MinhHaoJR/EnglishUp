import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import SignIn, { safeNext } from '../features/account/SignIn';
import Account from '../features/account/Account';
import { useAuth } from '../services/auth';
import { useAdmin } from '../services/admin';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(() => {
  fetchMock = vi.fn(() => Promise.resolve(json({}, 500)));
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
  useAdmin.setState({ isAdmin: false, checkedFor: null });
});

const show = (path: string) =>
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/login" element={<SignIn />} />
        <Route path="/account" element={<Account />} />
        <Route path="/game" element={<p>Game page</p>} />
        <Route path="/admin" element={<p>Admin page</p>} />
        <Route path="/" element={<p>Home page</p>} />
      </Routes>
    </MemoryRouter>,
  );
const submit = () => screen.getAllByRole('button', { name: /^(Đăng nhập|Tạo tài khoản)$/ }).at(-1)!;

test('only same-site paths are followed after signing in', () => {
  expect(safeNext('/game')).toBe('/game');
  expect(safeNext(null)).toBe('/');
  expect(safeNext('//evil.example')).toBe('/');
  expect(safeNext('https://evil.example')).toBe('/');
  expect(safeNext('/login?next=/game')).toBe('/');
});

test('signing in returns the learner to the page that sent them', async () => {
  fetchMock.mockImplementation((path: string) =>
    Promise.resolve(
      path === '/api/login'
        ? json({ accessToken: 'a', refreshToken: 'r', expiresIn: 3600 })
        : json({}, 500),
    ),
  );
  show('/login?next=/game');
  await userEvent.type(screen.getByRole('textbox', { name: 'Email' }), ' learner@example.test ');
  await userEvent.type(screen.getByLabelText('Mật khẩu'), 'Learn#2026');
  await userEvent.click(submit());
  expect(await screen.findByText('Game page')).toBeInTheDocument();
  expect(useAuth.getState().email).toBe('learner@example.test');
});

test('a wrong password explains what to do and keeps the form', async () => {
  fetchMock.mockImplementation(() => Promise.resolve(json({}, 401)));
  show('/login');
  await userEvent.type(screen.getByRole('textbox', { name: 'Email' }), 'learner@example.test');
  await userEvent.type(screen.getByLabelText('Mật khẩu'), 'nope');
  await userEvent.click(submit());
  expect(await screen.findByText(/Email hoặc mật khẩu không đúng/)).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: 'Chào mừng bạn quay lại' })).toBeInTheDocument();
});

test('creating an account shows which password rules are met, and the password can be shown', async () => {
  show('/login');
  await userEvent.click(screen.getByRole('button', { name: 'Tạo tài khoản', pressed: false }));
  const password = screen.getByLabelText('Mật khẩu');
  await userEvent.type(password, 'Learn2026');
  expect(screen.getByText('Ít nhất 8 ký tự').closest('li')).toHaveClass('met');
  expect(screen.getByText('Một chữ hoa').closest('li')).toHaveClass('met');
  expect(screen.getByText('Một ký tự đặc biệt').closest('li')).not.toHaveClass('met');
  expect(password).toHaveAttribute('autocomplete', 'new-password');

  await userEvent.click(screen.getByRole('button', { name: 'Hiện mật khẩu' }));
  expect(password).toHaveAttribute('type', 'text');
});

test('the account page sends signed-out learners to the sign-in page', () => {
  show('/account');
  expect(screen.getByRole('heading', { name: 'Mang tiến độ học theo bạn' })).toBeInTheDocument();
});

test('signed-in learners skip the sign-in page', async () => {
  useAuth.setState({ email: 'learner@example.test' });
  show('/login?next=/game');
  expect(await screen.findByText('Game page')).toBeInTheDocument();
});

test('an admin account goes to the admin page, a learner never does', async () => {
  fetchMock.mockImplementation((path: string) =>
    Promise.resolve(
      path === '/api/login'
        ? json({ accessToken: 'a', refreshToken: 'r', expiresIn: 3600 })
        : path === '/api/me'
          ? json({ email: 'boss@example.test', isAdmin: true })
          : json({}, 500),
    ),
  );
  show('/login?next=/game');
  await userEvent.type(screen.getByRole('textbox', { name: 'Email' }), 'boss@example.test');
  await userEvent.type(screen.getByLabelText('Mật khẩu'), 'Learn#2026');
  await userEvent.click(submit());
  expect(await screen.findByText('Admin page')).toBeInTheDocument();
});

test('a learner sent from the admin page lands on the learning app', async () => {
  useAuth.setState({ email: 'learner@example.test' });
  show('/login?next=/admin');
  expect(await screen.findByText('Home page')).toBeInTheDocument();
});
