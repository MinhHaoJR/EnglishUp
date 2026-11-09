import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import { structures } from '../data/content';
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
