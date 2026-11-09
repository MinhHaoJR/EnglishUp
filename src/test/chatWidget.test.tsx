import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Link, MemoryRouter } from 'react-router-dom';
import ChatWidget from '../features/assistant/ChatWidget';
import { useAuth } from '../services/auth';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

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
  fetchMock = vi.fn(() =>
    Promise.resolve(
      json({
        conversationId: '3f2a8c1e-5b7d-4e9a-8c6b-1d2e3f4a5b6c',
        answer: 'Routine là thói quen hằng ngày [1].',
        citations: [{ n: 1, sourceType: 'word', sourceId: 'v-1-1', title: 'routine', score: 0.8 }],
        questionsLeft: 19,
      }),
    ),
  );
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
});

const show = (path = '/') =>
  render(
    <MemoryRouter initialEntries={[path]}>
      <Link to="/reading">Đi tới bài đọc</Link>
      <ChatWidget />
    </MemoryRouter>,
  );
const toggle = () => screen.getByRole('button', { name: 'Trợ giảng AI' });

it('opens from the corner, sends with Enter and keeps the chat across pages', async () => {
  show();
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(toggle()).toHaveAttribute('aria-expanded', 'false');

  await userEvent.click(toggle());
  expect(screen.getByRole('dialog', { name: 'Trợ giảng AI' })).toBeInTheDocument();
  const box = screen.getByRole('textbox', { name: 'Câu hỏi của bạn' });
  expect(box).toHaveFocus();
  await userEvent.type(box, 'routine là gì?{Enter}');
  expect(await screen.findByText('Routine là thói quen hằng ngày [1].')).toBeInTheDocument();
  expect(screen.getByRole('link', { name: 'Từ vựng: routine' })).toHaveAttribute(
    'href',
    '/vocabulary',
  );

  await userEvent.click(screen.getByRole('link', { name: 'Đi tới bài đọc' }));
  expect(screen.getByText('Routine là thói quen hằng ngày [1].')).toBeInTheDocument();
});

it('Shift+Enter adds a line instead of sending', async () => {
  show();
  await userEvent.click(toggle());
  const box = screen.getByRole('textbox', { name: 'Câu hỏi của bạn' });
  await userEvent.type(box, 'dòng một{Shift>}{Enter}{/Shift}dòng hai');
  expect(box).toHaveValue('dòng một\ndòng hai');
  expect(fetchMock).not.toHaveBeenCalled();
});

it('closes with Escape and returns focus to the corner button', async () => {
  show();
  await userEvent.click(toggle());
  await userEvent.keyboard('{Escape}');
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  expect(toggle()).toHaveFocus();
});

it('asks signed-out learners to sign in and hides on the full tutor page', async () => {
  useAuth.setState({ email: null });
  const { unmount } = show();
  await userEvent.click(toggle());
  expect(screen.getByRole('link', { name: 'đăng nhập hoặc tạo tài khoản' })).toBeInTheDocument();
  unmount();

  show('/assistant');
  expect(screen.queryByRole('button', { name: 'Trợ giảng AI' })).not.toBeInTheDocument();
});

it('sends a suggested question and splits a long answer into bubbles', async () => {
  fetchMock.mockImplementation(() =>
    Promise.resolve(
      json({
        conversationId: '3f2a8c1e-5b7d-4e9a-8c6b-1d2e3f4a5b6c',
        answer: 'Routine là thói quen hằng ngày [1].\n\nHabit là việc bạn làm thường xuyên [2].',
        citations: [],
        questionsLeft: 18,
      }),
    ),
  );
  show();
  await userEvent.click(toggle());
  await userEvent.click(
    screen.getByRole('button', { name: '"routine" và "habit" khác nhau thế nào?' }),
  );

  const first = await screen.findByText('Routine là thói quen hằng ngày [1].');
  const second = screen.getByText('Habit là việc bạn làm thường xuyên [2].');
  expect(first).toHaveClass('bubble');
  expect(second).toHaveClass('bubble');
  expect(first.parentElement).toBe(second.parentElement);
  const body = JSON.parse((fetchMock.mock.calls[0] as [string, RequestInit])[1].body as string);
  expect(body.question).toBe('"routine" và "habit" khác nhau thế nào?');
  expect(screen.queryByRole('button', { name: /khác nhau thế nào/ })).not.toBeInTheDocument();
});
