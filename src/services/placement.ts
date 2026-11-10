import { quizzes, vocabulary } from '../data/content';
import { levelSchema, type Level } from '../data/schema';

export const LEVELS = levelSchema.options;
/** Questions per level: three grammar, two vocabulary (more vocabulary if a level lacks grammar). */
export const PER_LEVEL = 5;
const GRAMMAR_PER_LEVEL = 3;
/** A level counts as reached with at least this share right, on it and on every level below. */
export const PASS_SHARE = 0.6;

export type PlacementQuestion = {
  id: string;
  level: Level;
  kind: 'grammar' | 'word';
  /** A sentence with ___ (grammar) or an English word (vocabulary). */
  prompt: string;
  options: string[];
  answer: number;
};

const shuffle = <T>(items: T[], random: () => number) =>
  items
    .map((item) => ({ item, key: random() }))
    .sort((a, b) => a.key - b.key)
    .map(({ item }) => item);

/** Thirty questions from A1 to C2, easiest first, drawn from the live library. */
export function buildPlacement(random: () => number = Math.random): PlacementQuestion[] {
  return LEVELS.flatMap((level) => {
    const grammar = shuffle(
      quizzes.filter((q) => q.level === level),
      random,
    )
      .slice(0, GRAMMAR_PER_LEVEL)
      .map((q): PlacementQuestion => {
        const options = shuffle(q.options, random);
        return {
          id: q.id,
          level,
          kind: 'grammar',
          prompt: q.sentence,
          options,
          answer: options.indexOf(q.answer),
        };
      });
    const pool = vocabulary.filter((w) => w.level === level);
    const words = shuffle(pool, random)
      .slice(0, PER_LEVEL - grammar.length)
      .map((word): PlacementQuestion => {
        const others = shuffle(
          [...new Set(pool.map((w) => w.meaning))].filter((m) => m !== word.meaning),
          random,
        ).slice(0, 3);
        const options = shuffle([word.meaning, ...others], random);
        return {
          id: word.id,
          level,
          kind: 'word',
          prompt: word.word,
          options,
          answer: options.indexOf(word.meaning),
        };
      });
    return [...grammar, ...words];
  });
}

export type PlacementResult = {
  /** Out of 100. */
  score: number;
  correct: number;
  total: number;
  perLevel: { level: Level; correct: number; total: number; passed: boolean }[];
  /** The highest level passed with every level below it; null when even A1 was not passed. */
  level: Level | null;
};

/** Scores the answers (option index per question, -1 = skipped) and estimates the level. */
export function scorePlacement(questions: PlacementQuestion[], answers: number[]): PlacementResult {
  const right = questions.map((q, i) => answers[i] === q.answer);
  const correct = right.filter(Boolean).length;
  let level: Level | null = null;
  let climbing = true;
  const perLevel = LEVELS.map((lvl) => {
    const at = questions.flatMap((q, i) => (q.level === lvl ? [right[i]] : []));
    const got = at.filter(Boolean).length;
    const passed = at.length > 0 && got >= Math.ceil(at.length * PASS_SHARE);
    // The estimate stops at the first level not passed, so a lucky guess higher up does not count.
    if (climbing && passed) level = lvl;
    else if (at.length) climbing = false;
    return { level: lvl, correct: got, total: at.length, passed };
  });
  return {
    score: questions.length ? Math.round((correct / questions.length) * 100) : 0,
    correct,
    total: questions.length,
    perLevel,
    level,
  };
}

/** The path that starts at the estimated level (A1→A2 below A1; C2 learners keep the C1→C2 path). */
export function roadmapFor(level: Level | null) {
  const from = level === null ? 'A1' : level === 'C2' ? 'C1' : level;
  const to = LEVELS[LEVELS.indexOf(from) + 1];
  return `rm-${from.toLowerCase()}-${to.toLowerCase()}`;
}
