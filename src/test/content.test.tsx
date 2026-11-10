import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import ContentManager from '../features/admin/ContentManager';
import { readings, vocabulary } from '../data/content';
import { seedRows } from '../data/seed';
import { applyContent, loadContent, useContent, type ContentRow } from '../services/content';
import { useAuth } from '../services/auth';
import { db, resetData } from '../services/storage';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
const at = '2026-11-10T08:00:00Z';
const original = vocabulary[0];
const seedWords = vocabulary.length;
const seedReadings = readings.length;

afterEach(async () => {
  applyContent(seedRows);
  vi.unstubAllGlobals();
  localStorage.clear();
  useAuth.setState({ email: null });
  await db.lessons.clear();
});

test('the library follows the server rows; hidden and invalid rows never reach learners', () => {
  const firstReading = seedRows.find((r) => r.kind === 'reading')!.id;
  const rows: ContentRow[] = [
    // The first word is deleted on the server and the first reading hidden.
    ...seedRows
      .filter((r) => r.kind !== 'word' || r.id !== original.id)
      .map((r) => (r.kind === 'reading' && r.id === firstReading ? { ...r, hidden: true } : r)),
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
  ];
  applyContent(rows);
  expect(vocabulary.some((w) => w.id === original.id)).toBe(false);
  expect(vocabulary.at(-1)?.word).toBe('harbour');
  expect(vocabulary.some((w) => w.id === 'a-bad')).toBe(false);
  expect(vocabulary).toHaveLength(seedWords);
  expect(readings).toHaveLength(seedReadings - 1);
});

test('each download is kept on the device, so lessons still load offline', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn(() => Promise.resolve(json(seedRows))),
  );
  await loadContent(true);
  expect(useContent.getState().status).toBe('live');
  expect((await db.lessons.get('library'))?.rows).toHaveLength(seedRows.length);

  // A reset clears the learner's data, not the lesson library.
  await resetData();
  expect(await db.lessons.get('library')).toBeDefined();

  applyContent([]);
  vi.stubGlobal(
    'fetch',
    vi.fn(() => Promise.reject(new TypeError('offline'))),
  );
  await loadContent(true);
  expect(useContent.getState().status).toBe('offline');
  expect(vocabulary).toHaveLength(seedWords);

  await db.lessons.clear();
  await loadContent(true);
  expect(useContent.getState().status).toBe('missing');
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
    fetchMock = vi.fn((path: string, init?: RequestInit) =>
      Promise.resolve(
        path === '/api/content'
          ? json(seedRows)
          : init?.method === 'DELETE'
            ? new Response(null, { status: 204 })
            : json({ kind: 'word', id: 'x', data: {}, hidden: false, updatedAt: at }),
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

  it('groups words by topic into the 20-word learning clusters and lists every word', async () => {
    show();
    const daily = vocabulary.filter((w) => w.topic === 'Daily life');
    const topic = await screen.findByRole('button', { name: /^Đời sống/ });
    expect(topic).toHaveAttribute('aria-expanded', 'false');
    await userEvent.click(topic);
    const section = topic.closest('section')!;
    expect(within(section).getAllByRole('heading', { level: 4 })).toHaveLength(
      Math.ceil(daily.length / 20),
    );
    expect(within(section).getAllByRole('listitem')).toHaveLength(daily.length);

    // A search shows every match, not a first page, in its real cluster.
    await userEvent.type(screen.getByRole('searchbox'), 'v-');
    expect(
      await screen.findByText(`${vocabulary.length}/${vocabulary.length} mục khớp`, {
        exact: false,
      }),
    ).toBeInTheDocument();
    expect(document.querySelectorAll('.content-topics li')).toHaveLength(vocabulary.length);
  });

  it('lists every kind from the library and deletes only after a confirmation', async () => {
    show();
    // Sentence patterns are grouped like the grammar page, every pattern in its group.
    await userEvent.click(await screen.findByRole('tab', { name: /Cấu trúc câu/ }));
    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(12);
    await userEvent.click(screen.getByRole('button', { name: 'Mở tất cả' }));
    expect(document.querySelectorAll('.content-topics li')).toHaveLength(100);

    await userEvent.click(screen.getByRole('tab', { name: /Câu dịch/ }));
    const first = seedRows.find((r) => r.kind === 'translation')!;
    await userEvent.click(screen.getByRole('button', { name: /^Đời sống/ }));
    const row = (await screen.findByText(first.id)).closest('li')!;
    await userEvent.click(within(row).getByRole('button', { name: 'Xoá' }));
    expect(
      fetchMock.mock.calls.some(([, init]) => (init as RequestInit)?.method === 'DELETE'),
    ).toBe(false);
    await userEvent.click(within(row).getByRole('button', { name: 'Xác nhận xoá vĩnh viễn' }));
    const del = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === 'DELETE');
    expect(del![0]).toBe(`/api/admin/content/translation/${first.id}`);
  });
});
