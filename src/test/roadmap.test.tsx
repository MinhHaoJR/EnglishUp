import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import { seedRows } from '../data/seed';
import { parseRow } from '../services/content';
import { quizzes, roadmaps } from '../data/content';
import {
  buildPlacement,
  roadmapFor,
  scorePlacement,
  type PlacementQuestion,
} from '../services/placement';
import Placement from '../features/roadmap/Placement';
import Roadmap from '../features/roadmap/Roadmap';

beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'vi' },
    level: 'all',
    topic: 'all',
    ready: true,
  });
});

function Where() {
  const location = useLocation();
  return <p data-testid="where">{location.pathname + location.search}</p>;
}
const show = (element: React.ReactNode, path = '/') =>
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="*" element={element} />
      </Routes>
      <Where />
    </MemoryRouter>,
  );

test('every seed item, including the grammar questions and learning paths, is valid for the app', () => {
  expect(seedRows.filter((row) => parseRow(row) === null).map((row) => row.id)).toEqual([]);
  expect(quizzes).toHaveLength(133);
  expect(roadmaps.map((r) => `${r.from}-${r.to}`)).toEqual([
    'A1-A2',
    'A2-B1',
    'B1-B2',
    'B2-C1',
    'C1-C2',
  ]);
  for (const level of ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
    expect(quizzes.filter((q) => q.level === level).length).toBeGreaterThanOrEqual(15);
  // Each blank has exactly one right answer among four different options.
  for (const q of quizzes) expect(q.options.filter((o) => o === q.answer)).toHaveLength(1);
});

test('the level test has five questions per level, easiest first, each with its answer among the options', () => {
  const questions = buildPlacement(() => 0.5);
  expect(questions).toHaveLength(30);
  expect(questions.map((q) => q.level)).toEqual(
    ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].flatMap((l) => Array(5).fill(l)),
  );
  expect(questions.filter((q) => q.kind === 'grammar')).toHaveLength(18);
  for (const q of questions) {
    expect(q.options).toHaveLength(4);
    expect(q.answer).toBeGreaterThanOrEqual(0);
  }
});

test('the estimated level is the highest one passed with every level below it', () => {
  const questions = buildPlacement();
  const answerUpTo = (
    levels: string[],
    extra: (q: PlacementQuestion, i: number) => boolean = () => false,
  ) => questions.map((q, i) => (levels.includes(q.level) || extra(q, i) ? q.answer : -1));

  const b1 = scorePlacement(questions, answerUpTo(['A1', 'A2', 'B1']));
  expect(b1).toMatchObject({ level: 'B1', correct: 15, score: 50 });
  expect(b1.perLevel.map((l) => l.passed)).toEqual([true, true, true, false, false, false]);

  // Lucky answers above a failed level do not raise the estimate.
  const lucky = scorePlacement(
    questions,
    answerUpTo(['A1', 'A2'], (q) => q.level === 'C1'),
  );
  expect(lucky.level).toBe('A2');

  // Three of five is enough for a level.
  const three = scorePlacement(
    questions,
    answerUpTo([], (q, i) => q.level === 'A1' && i < 3),
  );
  expect(three.level).toBe('A1');
  expect(scorePlacement(questions, Array(30).fill(-1))).toMatchObject({ level: null, score: 0 });
  expect(
    scorePlacement(
      questions,
      questions.map((q) => q.answer),
    ),
  ).toMatchObject({ level: 'C2', score: 100 });

  expect(roadmapFor(null)).toBe('rm-a1-a2');
  expect(roadmapFor('B1')).toBe('rm-b1-b2');
  expect(roadmapFor('C2')).toBe('rm-c1-c2');
});

test('taking the level test saves the result and points to the matching learning path', async () => {
  show(<Placement />, '/placement');
  await userEvent.click(screen.getByRole('button', { name: 'Bắt đầu kiểm tra' }));
  for (let i = 0; i < 30; i++) {
    expect(screen.getByText(`Câu ${i + 1}/30`)).toBeInTheDocument();
    await userEvent.click(screen.getByRole('button', { name: 'Bỏ qua câu này' }));
  }
  expect(await screen.findByRole('heading', { name: 'Kết quả của bạn' })).toBeInTheDocument();
  expect(screen.getByText('Dưới A1')).toBeInTheDocument();
  await waitFor(() =>
    expect(useApp.getState().settings.placement).toMatchObject({ level: null, score: 0 }),
  );
  expect((await db.attempts.toArray()).map((a) => a.skill)).toEqual(['grammar']);
  await userEvent.click(screen.getByRole('link', { name: /Xem lộ trình A1 → A2/ }));
  expect(screen.getByTestId('where')).toHaveTextContent('/roadmap?path=rm-a1-a2');
});

test('a learning path suggests itself from the level test, tracks ticked tasks and opens practice at the level', async () => {
  useApp.setState({
    settings: {
      ...defaults,
      language: 'vi',
      placement: { level: 'B1', score: 55, at: Date.now() },
    },
  });
  show(<Roadmap />, '/roadmap');
  expect(
    screen.getByRole('heading', { name: 'Từ B1 lên B2: diễn đạt ý kiến rõ ràng' }),
  ).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /B1\s*B2\s*Gợi ý cho bạn/ })).toHaveAttribute(
    'aria-current',
    'step',
  );

  const stage = screen.getByRole('region', { name: /Chặng 1/ });
  const boxes = within(stage).getAllByRole('checkbox');
  await userEvent.click(boxes[0]);
  await waitFor(() =>
    expect(useApp.getState().settings.roadmap).toEqual({
      id: 'rm-b1-b2',
      done: { 'rm-b1-b2': ['s1t1'] },
    }),
  );
  expect(screen.getByText('1/12 nhiệm vụ xong')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /B1\s*B2\s*Đang theo/ })).toBeInTheDocument();

  // A grammar race task opens the race at its level and grammar point, and sets the shared level filter.
  const stage2 = screen.getByRole('region', { name: /Chặng 2/ });
  const race = within(stage2)
    .getByText(/dạng Câu điều kiện/)
    .closest('li')!;
  await userEvent.click(within(race).getByRole('button', { name: /Mở bài luyện/ }));
  expect(screen.getByTestId('where')).toHaveTextContent(
    '/game?mode=grammar&level=B1&category=conditional',
  );
  expect(useApp.getState().level).toBe('B1');
});
