import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ContentManager from '../features/admin/ContentManager';
import { readings, vocabulary } from '../data/content';
import { applyContent, bundled, type ContentRow } from '../services/content';
import { useAuth } from '../services/auth';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
const at = '2026-11-10T08:00:00Z';
const original = bundled.word[0] as (typeof vocabulary)[number];

afterEach(() => {
  applyContent([]);
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
});

test('admin rows replace, add and hide items; invalid rows never reach learners', () => {
  const rows: ContentRow[] = [
    {
      kind: 'word',
      id: original.id,
      data: { ...original, meaning: 'đã sửa' },
      hidden: false,
      updatedAt: at,
    },
    {
      kind: 'word',
      id: 'a-new',
      data: { ...original, id: 'a-new', word: 'harbour' },
      hidden: false,
      updatedAt: at,
    },
    {
      kind: 'word',
      id: 'a-bad',
      data: { id: 'a-bad', word: 'broken' },
      hidden: false,
      updatedAt: at,
    },
    { kind: 'reading', id: bundled.reading[0].id, hidden: true, updatedAt: at },
  ];
  applyContent(rows);
  expect(vocabulary.find((w) => w.id === original.id)?.meaning).toBe('đã sửa');
  expect(vocabulary.at(-1)?.word).toBe('harbour');
  expect(vocabulary.some((w) => w.id === 'a-bad')).toBe(false);
  expect(readings).toHaveLength(bundled.reading.length - 1);

  applyContent([]);
  expect(vocabulary).toHaveLength(bundled.word.length);
  expect(vocabulary[0].meaning).toBe(original.meaning);
});

describe('content manager', () => {
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
    fetchMock = vi.fn((path: string) =>
      Promise.resolve(
        path === '/api/content'
          ? json([])
          : json({ kind: 'word', id: 'x', hidden: false, updatedAt: at }),
      ),
    );
    vi.stubGlobal('fetch', fetchMock);
  });
  const show = () =>
    render(
      <MemoryRouter>
        <ContentManager />
      </MemoryRouter>,
    );

  it('adds a word through the form and sends it to the server', async () => {
    show();
    await userEvent.click(await screen.findByRole('button', { name: '+ Thêm từ vựng' }));
    const form = screen.getByRole('heading', { name: /Thêm mục mới/ }).closest('form')!;
    await userEvent.clear(within(form).getByLabelText('Từ'));
    await userEvent.type(within(form).getByLabelText('Từ'), 'harbour');
    await userEvent.clear(within(form).getByLabelText('Nghĩa tiếng Việt'));
    await userEvent.type(within(form).getByLabelText('Nghĩa tiếng Việt'), 'bến cảng');
    expect(within(form).getByText(/Hợp lệ với cấu trúc/)).toBeInTheDocument();
    await userEvent.click(within(form).getByRole('button', { name: 'Lưu' }));

    const put = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === 'PUT');
    expect(put![0]).toMatch(/^\/api\/admin\/content\/word\/a-word-/);
    const body = JSON.parse((put![1] as RequestInit).body as string);
    expect(body.data).toMatchObject({
      word: 'harbour',
      meaning: 'bến cảng',
      level: original.level,
    });
    expect(await screen.findByText(/Đã lưu/)).toBeInTheDocument();
  });

  it('checks JSON lessons against the app schema before saving', async () => {
    show();
    await userEvent.click(await screen.findByRole('tab', { name: /Bài đọc/ }));
    await userEvent.click(screen.getByRole('button', { name: '+ Thêm bài đọc' }));
    const editor = screen.getByRole('textbox', { name: /Nội dung \(JSON/ });
    await userEvent.clear(editor);
    await userEvent.type(editor, '{{"id": "r-x", "title": "Only a title"}');
    expect(screen.getByText(/^level:/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Lưu' })).toBeDisabled();
  });
});
