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

const post = (body?: unknown): RequestInit => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: body === undefined ? undefined : JSON.stringify(body),
});

/** The server draws the questions and keeps the answers; level null means every level. */
export const startGame = (level: string | null) =>
  fetchJson(startSchema, '/api/game/start', post({ level }));

/** Rejects with ApiError 409 once the server's 60 seconds are over. */
export const answerQuestion = (id: string, index: number, choice: number) =>
  fetchJson(answerSchema, `/api/game/${id}/answer`, post({ index, choice }));

export const finishGame = (id: string) => fetchJson(resultSchema, `/api/game/${id}/finish`, post());

export const fetchRecords = () => fetchJson(recordsSchema, '/api/game/records');
