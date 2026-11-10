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
    const save = within(form).getByRole('button', { name: 'Lưu vào cơ sở dữ liệu' });
    // A new item starts blank, so it cannot be saved yet.
    expect(save).toBeDisabled();
    for (const [name, text] of [
      ['Từ', 'harbour'],
      ['Từ loại', 'noun'],
      ['Nghĩa tiếng Việt', 'bến cảng'],
      ['Định nghĩa tiếng Anh', 'A sheltered place for boats.'],
      [/^Ví dụ/, 'The boats wait in the harbour.'],
    ] as const)
      await userEvent.type(within(form).getByLabelText(name), text);
    await userEvent.selectOptions(within(form).getByLabelText('Trình độ'), 'B1');
    expect(within(form).getByText(/Hợp lệ với cấu trúc/)).toBeInTheDocument();
    await userEvent.click(save);

    const put = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === 'PUT');
    expect(put![0]).toMatch(/^\/api\/admin\/content\/word\/a-word-/);
    const body = JSON.parse((put![1] as RequestInit).body as string);
    expect(body.data).toMatchObject({
      word: 'harbour',
      meaning: 'bến cảng',
      examples: ['The boats wait in the harbour.'],
      level: 'B1',
      topic: 'Daily life',
    });
    expect(await screen.findByText(/Đã lưu/)).toBeInTheDocument();
  });

  it('gives lessons a form with repeatable questions, checked against the app schema', async () => {
    show();
    await userEvent.click(await screen.findByRole('tab', { name: /Bài đọc/ }));
    await userEvent.click(screen.getByRole('button', { name: '+ Thêm bài đọc' }));
    const form = screen.getByRole('heading', { name: /Thêm mục mới/ }).closest('form')!;
    // No JSON: the passage and its five questions are separate fields.
    expect(within(form).queryByText(/JSON/)).not.toBeInTheDocument();
    expect(within(form).getByLabelText('Bài đọc')).toBeInTheDocument();
    expect(within(form).getAllByLabelText('Câu hỏi')).toHaveLength(5);
    expect(within(form).getByText('Chưa điền: Tiêu đề')).toBeInTheDocument();
    expect(within(form).getByRole('button', { name: 'Lưu vào cơ sở dữ liệu' })).toBeDisabled();

    // A sixth question can be added and removed again; a reading needs exactly five.
    await userEvent.click(within(form).getByRole('button', { name: '+ Thêm mục' }));
    expect(within(form).getAllByLabelText('Câu hỏi')).toHaveLength(6);
    await userEvent.click(within(form).getByRole('button', { name: 'Bỏ mục 6' }));
    expect(within(form).getAllByLabelText('Câu hỏi')).toHaveLength(5);
  });

  it('edits an existing lesson in its form and saves the change', async () => {
    show();
    await userEvent.click(await screen.findByRole('tab', { name: /Bài đọc/ }));
    await userEvent.click(screen.getByRole('button', { name: 'Mở tất cả' }));
    const first = readings[0];
    const row = screen.getByText(first.id).closest('li')!;
    await userEvent.click(within(row).getByRole('button', { name: 'Sửa' }));
    const form = screen.getByRole('heading', { name: /Sửa mục/ }).closest('form')!;
    const titleBox = within(form).getByLabelText('Tiêu đề');
    expect(titleBox).toHaveValue(first.title);
    await userEvent.clear(titleBox);
    await userEvent.type(titleBox, 'A calmer morning');
    await userEvent.click(within(form).getByRole('button', { name: 'Lưu vào cơ sở dữ liệu' }));

    const put = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === 'PUT');
    expect(put![0]).toBe(`/api/admin/content/reading/${first.id}`);
    const body = JSON.parse((put![1] as RequestInit).body as string);
    expect(body.data).toEqual({ ...first, title: 'A calmer morning' });
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
