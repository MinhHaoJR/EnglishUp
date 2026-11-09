import { recommend } from './recommend';
import type { Attempt } from './storage';

const now = +new Date(2026, 10, 30, 12);
const daysAgo = (days: number) => now - days * 86_400_000;
let next = 0;
const attempt = (skill: Attempt['skill'], score: number, days: number): Attempt => ({
  id: String(next++),
  skill,
  score,
  duration: 60,
  timestamp: daysAgo(days),
  label: 'test',
});

test('a new learner starts with untried skills in skill order', () => {
  expect(recommend([], 0, now).map((r) => [r.skill, r.reason.kind])).toEqual([
    ['vocabulary', 'new'],
    ['listening', 'new'],
    ['speaking', 'new'],
  ]);
});

test('due cards lead, then the weakest and longest-unpractised skills', () => {
  const attempts = [
    ...(['vocabulary', 'listening', 'speaking', 'reading', 'writing', 'grammar'] as const).map(
      (s) => attempt(s, 90, 1),
    ),
    attempt('writing', 30, 1),
    attempt('reading', 95, 6),
    attempt('reading', 95, 5),
  ];
  const plan = recommend(attempts, 12, now);
  expect(plan[0]).toEqual({ skill: 'vocabulary', reason: { kind: 'due', cards: 12 }, minutes: 3 });
  // writing averages 60 (need 45); reading's 93 average was last practised 1 day ago (need 12).
  expect(plan[1]).toMatchObject({ skill: 'writing', reason: { kind: 'weak', average: 60 } });
  expect(plan).toHaveLength(3);
});

test('a strong but neglected skill outranks a recent one and reports the gap', () => {
  const plan = recommend(
    [
      attempt('vocabulary', 90, 0.9),
      attempt('listening', 90, 0.9),
      attempt('speaking', 90, 0.9),
      attempt('reading', 90, 0.9),
      attempt('grammar', 90, 0.9),
      attempt('writing', 85, 8),
    ],
    0,
    now,
    1,
  );
  expect(plan).toEqual([{ skill: 'writing', reason: { kind: 'stale', days: 8 }, minutes: 5 }]);
});

test('only the latest attempts count and today does not reshuffle the plan', () => {
  const old = Array.from({ length: 5 }, (_, i) => attempt('listening', 10, 20 + i));
  const recent = Array.from({ length: 5 }, () => attempt('listening', 100, 1));
  const today = attempt('speaking', 100, 0);
  const plan = recommend([...old, ...recent, today], 0, now, 6);
  expect(plan.find((r) => r.skill === 'listening')?.reason).toEqual({
    kind: 'keep',
    average: 100,
  });
  expect(plan.find((r) => r.skill === 'speaking')?.reason).toEqual({ kind: 'new' });
});
