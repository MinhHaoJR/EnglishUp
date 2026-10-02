import { schedule, dueQueue } from './srs';
import { vocabulary } from '../data/content';
test('SM-2 intervals, failures and minimum ease', () => {
  const first = schedule('a', 'good', undefined, 1000);
  expect(first.interval).toBe(1);
  const second = schedule('a', 'good', first, 2000);
  expect(second.interval).toBe(6);
  expect(schedule('a', 'easy', second, 3000).interval).toBe(15);
  const failed = schedule('a', 'again', second, 4000);
  expect(failed.repetitions).toBe(0);
  expect(failed.interval).toBe(1);
  let r = failed;
  for (let i = 0; i < 20; i++) r = schedule('a', 'again', r);
  expect(r.ease).toBe(1.3);
});
test('new limit is global while overdue cards are always included', () => {
  const now = Date.now();
  const review = schedule(vocabulary[0].id, 'good', undefined, now);
  review.due = now - 1;
  expect(dueQueue(vocabulary, [review], 1, now).map((w) => w.id)).toEqual([review.id]);
  expect(dueQueue(vocabulary, [], 0, now)).toEqual([]);
});
