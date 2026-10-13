import type { Word } from '../data/schema';
import type { Review } from './storage';
export type Rating = 'again' | 'hard' | 'good' | 'easy';
export const quality: Record<Rating, number> = { again: 1, hard: 3, good: 4, easy: 5 };
export function dayKey(time = Date.now()) {
  const d = new Date(time);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
export function schedule(id: string, rating: Rating, previous?: Review, now = Date.now()): Review {
  const q = quality[rating];
  let repetitions = previous?.repetitions ?? 0;
  let interval = previous?.interval ?? 0;
  const oldEase = previous?.ease ?? 2.5;
  const ease = Math.max(1.3, oldEase + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)));
  if (q < 3) {
    repetitions = 0;
    interval = 1;
  } else {
    interval =
      repetitions === 0 ? 1 : repetitions === 1 ? 6 : Math.max(1, Math.round(interval * oldEase));
    repetitions++;
  }
  const due = new Date(now);
  due.setDate(due.getDate() + interval);
  return {
    id,
    ease,
    interval,
    repetitions,
    due: due.getTime(),
    introduced: previous?.introduced ?? now,
    lastReviewed: now,
    correct: (previous?.correct ?? 0) + (q >= 3 ? 1 : 0),
    total: (previous?.total ?? 0) + 1,
  };
}
export function dueQueue(words: Word[], reviews: Review[], now = Date.now()) {
  const map = new Map(reviews.map((r) => [r.id, r]));
  const due = words
    .filter((w) => map.has(w.id) && map.get(w.id)!.due <= now)
    .sort((a, b) => map.get(a.id)!.due - map.get(b.id)!.due);
  const fresh = words.filter((w) => !map.has(w.id));
  return [...due, ...fresh];
}
