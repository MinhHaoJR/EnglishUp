import { z } from 'zod';
import { fetchJson } from './auth';

const startSchema = z.object({
  id: z.string().uuid(),
  durationSeconds: z.number().int().positive(),
  questions: z
    .array(z.object({ word: z.string().min(1), options: z.array(z.string()).length(4) }))
    .min(1),
});
export type GameStart = z.infer<typeof startSchema>;

const answerSchema = z.object({
  correct: z.boolean(),
  answer: z.number().int().min(0).max(3),
  combo: z.number().int().nonnegative(),
  score: z.number().int().nonnegative(),
  /** Why the answer is right; grammar questions only. */
  explanation: z.string().optional(),
});
export type GameAnswer = z.infer<typeof answerSchema>;

const count = z.number().int().nonnegative();
const resultSchema = z.object({
  score: count,
  correct: count,
  answered: count,
  maxCombo: count,
  pointsEarned: count,
  best: count,
  isRecord: z.boolean(),
});
export type GameResult = z.infer<typeof resultSchema>;

const recordsSchema = z.object({ best: count, played: count });
export type GameRecords = z.infer<typeof recordsSchema>;

/** vocabulary: pick a word's meaning; grammar: fill the blank in a sentence. Each has its own records and board. */
export type GameMode = 'vocabulary' | 'grammar';
export type GamePeriod = 'week' | 'all';
const leaderboardSchema = z.object({
  mode: z.enum(['vocabulary', 'grammar']),
  period: z.enum(['week', 'all']),
  entries: z.array(
    z.object({
      rank: z.number().int().positive(),
      displayName: z.string(),
      best: count,
      played: count,
      isMe: z.boolean(),
    }),
  ),
  myBest: count,
  myRowShown: z.boolean(),
});
export type GameLeaderboard = z.infer<typeof leaderboardSchema>;

const post = (body?: unknown): RequestInit => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: body === undefined ? undefined : JSON.stringify(body),
});

/** The server draws the questions and keeps the answers; null level or category means any. */
export const startGame = (
  level: string | null,
  mode: GameMode = 'vocabulary',
  category: string | null = null,
) => fetchJson(startSchema, '/api/game/start', post({ level, mode, category }));

/** Rejects with ApiError 409 once the server's 60 seconds are over. */
export const answerQuestion = (id: string, index: number, choice: number) =>
  fetchJson(answerSchema, `/api/game/${id}/answer`, post({ index, choice }));

export const finishGame = (id: string) => fetchJson(resultSchema, `/api/game/${id}/finish`, post());

export const fetchRecords = (mode: GameMode = 'vocabulary') =>
  fetchJson(recordsSchema, `/api/game/records?mode=${mode}`);

/** Each learner's best game this week (Monday, Vietnam time) or ever; hidden profiles are left out. */
export const fetchGameLeaderboard = (mode: GameMode, period: GamePeriod) =>
  fetchJson(leaderboardSchema, `/api/game/leaderboard?mode=${mode}&period=${period}`);
