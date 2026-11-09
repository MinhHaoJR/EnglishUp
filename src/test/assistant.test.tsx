import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Assistant from '../features/assistant/Assistant';
import { useAuth } from '../services/auth';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const conversationId = '3f2a8c1e-5b7d-4e9a-8c6b-1d2e3f4a5b6c';
const citation = { n: 1, sourceType: 'word', sourceId: 'v-1-1', title: 'routine', score: 0.81 };
let conversations: unknown[] = [];

function serve(askStatus = 200) {
  fetchMock.mockImplementation((path: string, init?: RequestInit) => {
    if (path === '/api/assistant/ask') {
      if (askStatus !== 200) return Promise.resolve(json({}, askStatus));
      conversations = [
        { id: conversationId, title: 'routine là gì?', updatedAt: '2026-11-09T09:00:00Z' },
      ];
      return Promise.resolve(
        json({
          conversationId,
          answer: 'Routine là thói quen hằng ngày [1].',
          citations: [citation],
          questionsLeft: 19,
        }),
      );
    }
    if (path === '/api/assistant/conversations') return Promise.resolve(json(conversations));
    if (path === `/api/assistant/conversations/${conversationId}`) {
      if (init?.method === 'DELETE') {
        conversations = [];
        return Promise.resolve(new Response(null, { status: 204 }));
      }
      return Promise.resolve(
        json([
          {
            role: 'user',
            content: 'Cũ: habit là gì?',
            createdAt: '2026-11-09T09:00:00Z',
            citations: [],
          },
          {
            role: 'assistant',
            content: 'Habit là thói quen [1].',
            createdAt: '2026-11-09T09:00:01Z',
            citations: [{ ...citation, sourceId: 'v-1-8', title: 'habit' }],
          },
        ]),
      );
    }
    return Promise.resolve(json({}, 404));
  });
}

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
  conversations = [];
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
      <Assistant />
    </MemoryRouter>,
  );

it('asks signed-out learners to sign in', () => {
  useAuth.setState({ email: null });
  show();
  expect(screen.getByRole('link', { name: 'đăng nhập hoặc tạo tài khoản' })).toBeInTheDocument();
  expect(fetchMock).not.toHaveBeenCalled();
});

it('shows a cited answer and lists the new conversation', async () => {
  serve();
  show();
  await userEvent.type(screen.getByRole('textbox', { name: 'Câu hỏi của bạn' }), 'routine là gì?');
  await userEvent.click(screen.getByRole('button', { name: 'Gửi' }));

  expect(await screen.findByText('Routine là thói quen hằng ngày [1].')).toBeInTheDocument();
  const sources = screen.getByRole('list', { name: 'Nguồn' });
  expect(within(sources).getByRole('link', { name: 'Từ vựng: routine' })).toHaveAttribute(
    'href',
    '/vocabulary',
  );
  expect(screen.getByText('Còn 19 câu hỏi hôm nay')).toBeInTheDocument();
  expect(screen.getByRole('textbox', { name: 'Câu hỏi của bạn' })).toHaveValue('');
  expect(await screen.findByRole('button', { name: 'routine là gì?' })).toBeInTheDocument();
  const body = JSON.parse(
    (fetchMock.mock.calls.find(([p]) => p === '/api/assistant/ask')![1] as RequestInit)
      .body as string,
  );
  expect(body).toEqual({ question: 'routine là gì?', conversationId: null });
});

it('keeps the question and explains a used-up daily limit', async () => {
  serve(429);
  show();
  await userEvent.type(screen.getByRole('textbox', { name: 'Câu hỏi của bạn' }), 'Một câu nữa');
  await userEvent.click(screen.getByRole('button', { name: 'Gửi' }));

  expect(await screen.findByText(/hết số câu hỏi hôm nay/)).toBeInTheDocument();
  expect(screen.getByRole('textbox', { name: 'Câu hỏi của bạn' })).toHaveValue('Một câu nữa');
  expect(screen.queryByText('Một câu nữa', { selector: 'p' })).not.toBeInTheDocument();
});

it('opens, continues and deletes a saved conversation', async () => {
  serve();
  conversations = [
    { id: conversationId, title: 'Cũ: habit là gì?', updatedAt: '2026-11-09T09:00:00Z' },
  ];
  show();
  await userEvent.click(await screen.findByRole('button', { name: 'Cũ: habit là gì?' }));
  expect(await screen.findByText('Habit là thói quen [1].')).toBeInTheDocument();

  await userEvent.type(screen.getByRole('textbox', { name: 'Câu hỏi của bạn' }), 'Còn routine?');
  await userEvent.click(screen.getByRole('button', { name: 'Gửi' }));
  await screen.findByText('Routine là thói quen hằng ngày [1].');
  const body = JSON.parse(
    (fetchMock.mock.calls.find(([p]) => p === '/api/assistant/ask')![1] as RequestInit)
      .body as string,
  );
  expect(body.conversationId).toBe(conversationId);

  await userEvent.click(screen.getByRole('button', { name: 'Xoá: routine là gì?' }));
  await waitFor(() => expect(screen.getByText('Chưa có cuộc trò chuyện nào.')).toBeInTheDocument());
  expect(screen.queryByText('Habit là thói quen [1].')).not.toBeInTheDocument();
});
