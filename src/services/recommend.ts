import type { Skill } from '../data/schema';
import { skills } from './progress';
import { dayKey } from './srs';
import type { Attempt } from './storage';

/** Why a skill is suggested; the dashboard turns this into a bilingual sentence. */
export type Reason =
  | { kind: 'due'; cards: number }
  | { kind: 'new' }
  | { kind: 'weak'; average: number }
  | { kind: 'stale'; days: number }
  | { kind: 'keep'; average: number };
export type Recommendation = { skill: Skill; reason: Reason; minutes: number };

/** Averages use only the latest attempts so old results stop counting once a learner improves. */
export const RECENT = 5;
export const WEAK_BELOW = 70;
export const STALE_DAYS = 3;
const minutes: Record<Skill, number> = {
  vocabulary: 3,
  listening: 4,
  speaking: 3,
  reading: 3,
  writing: 5,
};
const DAY = 86_400_000;

/**
 * Ranks skills by need = (100 − recent average) + 5 per day since last practice (up to 14 days).
 * Untried skills come first, and due review cards always lead the plan.
 * Only attempts before today count, so the plan stays fixed while the learner works through it.
 */
export function recommend(
  attempts: Attempt[],
  dueCards: number,
  now = Date.now(),
  limit = 3,
): Recommendation[] {
  const today = dayKey(now);
  const before = attempts.filter((a) => dayKey(a.timestamp) !== today && a.timestamp < now);
  const picks: Recommendation[] =
    dueCards > 0
      ? [{ skill: 'vocabulary', reason: { kind: 'due', cards: dueCards }, minutes: 3 }]
      : [];
  const ranked = skills
    .filter((skill) => !picks.some((p) => p.skill === skill))
    .map((skill, order) => {
      const recent = before
        .filter((a) => a.skill === skill)
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(0, RECENT);
      if (!recent.length) return { skill, reason: { kind: 'new' } as Reason, need: 1000, order };
      const average = Math.round(recent.reduce((sum, a) => sum + a.score, 0) / recent.length);
      const days = Math.floor((now - recent[0].timestamp) / DAY);
      const reason: Reason =
        average < WEAK_BELOW
          ? { kind: 'weak', average }
          : days >= STALE_DAYS
            ? { kind: 'stale', days }
            : { kind: 'keep', average };
      return { skill, reason, need: 100 - average + 5 * Math.min(days, 14), order };
    })
    .sort((a, b) => b.need - a.need || a.order - b.order);
  for (const { skill, reason } of ranked) picks.push({ skill, reason, minutes: minutes[skill] });
  return picks.slice(0, limit);
}
