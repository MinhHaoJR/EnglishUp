import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import { structures, tenses } from '../data/content';
import userEvent from '@testing-library/user-event';
import Grammar from '../features/grammar/Grammar';

beforeEach(async () => {
  await resetData();
  useApp.setState({ settings: { ...defaults, language: 'vi' }, ready: true });
});

const show = () =>
  render(
    <MemoryRouter>
      <Grammar />
    </MemoryRouter>,
  );

test('the pattern catalogue has 100 original entries the quiz can blank out', () => {
  expect(structures).toHaveLength(100);
  for (const s of structures) {
    expect(s.example.split(s.key)).toHaveLength(2);
    expect(new Set([s.key, ...s.options]).size).toBe(3);
  }
});

test('learners can browse, filter and search the patterns', () => {
  show();
  expect(screen.getByRole('status')).toHaveTextContent('Đang hiện 100 / 100 cấu trúc');
  fireEvent.change(screen.getByRole('combobox', { name: 'Nhóm cấu trúc' }), {
    target: { value: 'v-ing' },
  });
  expect(screen.getByRole('status')).toHaveTextContent('Đang hiện 10 / 100 cấu trúc');
  fireEvent.change(screen.getByRole('searchbox', { name: 'Tìm cấu trúc' }), {
    target: { value: 'enjoy' },
  });
  const card = screen.getByRole('heading', { name: 'Enjoy + V-ing' }).closest('article')!;
  expect(within(card).getByText('enjoys painting').tagName).toBe('MARK');
  expect(within(card).getByText('Mai thích vẽ tranh vào sáng Chủ nhật.')).toBeInTheDocument();
  expect(screen.getByRole('status')).toHaveTextContent('Đang hiện 1 / 100 cấu trúc');
});

test('practice blanks the pattern, marks answers and saves the attempt', async () => {
  show();
  fireEvent.change(screen.getByRole('combobox', { name: 'Nhóm cấu trúc' }), {
    target: { value: 'degree' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Luyện tập' }));
  const group = structures.filter((s) => s.group === 'degree');

  for (let i = 0; i < group.length; i++) {
    expect(screen.getByText(`Câu ${i + 1} / ${group.length} · Quá… / đủ…`)).toBeInTheDocument();
    const hint = screen.getByText(/^Gợi ý nghĩa:/).textContent!;
    const s = group.find((item) => hint.endsWith(item.translation))!;
    // Answer the first question wrongly, the rest correctly.
    fireEvent.click(screen.getByRole('button', { name: i === 0 ? s.options[0] : s.key }));
    if (i === 0) {
      expect(screen.getByRole('status')).toHaveTextContent(`Chưa đúng. Đáp án: ${s.key}`);
      expect(screen.getByRole('button', { name: `${s.key} ✓` })).toBeDisabled();
    } else expect(screen.getByRole('status')).toHaveTextContent('Đúng!');
    fireEvent.click(
      screen.getByRole('button', { name: i + 1 < group.length ? 'Câu tiếp' : 'Xem kết quả' }),
    );
  }

  expect(await screen.findByRole('heading', { name: 'Kết quả: 4 / 5' })).toBeInTheDocument();
  await waitFor(async () => {
    const [attempt] = await db.attempts.where('skill').equals('grammar').toArray();
    expect(attempt).toMatchObject({ score: 80, label: 'Cấu trúc câu · Quá… / đủ…' });
  });
});

test('the tenses cover the twelve tenses plus be going to, each with a check that has one right answer', () => {
  expect(tenses).toHaveLength(13);
  expect(tenses.filter((t) => t.group === 'present')).toHaveLength(4);
  expect(tenses.filter((t) => t.group === 'past')).toHaveLength(4);
  expect(tenses.filter((t) => t.group === 'future')).toHaveLength(5);
  for (const tense of tenses)
    for (const q of tense.practice) expect(q.options.filter((o) => o === q.answer)).toHaveLength(1);
});

test('the grammar page has a tenses part: pick a tense, read its form, take the quick check', async () => {
  show();
  expect(screen.getByRole('heading', { name: 'Ngữ pháp', level: 1 })).toBeInTheDocument();
  await userEvent.click(screen.getByRole('tab', { name: /Các thì/ }));
  // The timeline starts with the first tense; another one opens from its time column.
  expect(screen.getByRole('heading', { name: 'Hiện tại đơn', level: 2 })).toBeInTheDocument();
  const past = screen.getByRole('heading', { name: 'Quá khứ' }).closest('section')!;
  await userEvent.click(within(past).getByRole('button', { name: /Quá khứ đơn/ }));
  const card = screen.getByRole('article');
  expect(within(card).getByRole('heading', { name: 'Quá khứ đơn' })).toBeInTheDocument();
  expect(within(card).getByText('S + V2/ed')).toBeInTheDocument();
  expect(within(card).getByText('yesterday')).toBeInTheDocument();

  // Answer the three checks: the right one, then two wrong ones.
  const tense = tenses.find((t) => t.id === 't-past-simple')!;
  const check = within(card).getByRole('heading', { name: 'Luyện nhanh' }).closest('section')!;
  const items = within(check).getAllByRole('listitem');
  for (const [i, q] of tense.practice.entries()) {
    const pick = i === 0 ? q.answer : q.options.find((o) => o !== q.answer)!;
    await userEvent.click(within(items[i]).getByRole('button', { name: pick }));
  }
  expect(within(check).getByText(/Kết quả: 1\/3 câu đúng/)).toBeInTheDocument();
  await waitFor(async () => {
    const [attempt] = await db.attempts.toArray();
    expect(attempt).toMatchObject({
      skill: 'grammar',
      score: 33,
      label: 'Các thì / Tenses · Past simple',
    });
  });
});
