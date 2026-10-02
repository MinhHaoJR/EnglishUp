import Dexie, { type Table } from 'dexie';
import { z } from 'zod';
import { skillSchema, wordSchema, type Word, type Skill } from '../data/schema';
export const settingsSchema = z.object({
  id: z.literal('main'),
  language: z.enum(['vi', 'en']),
  accent: z.enum(['en-US', 'en-GB']),
  rate: z.number().min(0.5).max(1.5),
  theme: z.enum(['light', 'dark']),
  dailyGoal: z.number().int().min(1).max(120),
  newCards: z.number().int().min(0).max(100),
  transcript: z.boolean(),
});
export type Settings = z.infer<typeof settingsSchema>;
export const defaults: Settings = {
  id: 'main',
  language: 'vi',
  accent: 'en-US',
  rate: 1,
  theme: 'light',
  dailyGoal: 10,
  newCards: 10,
  transcript: false,
};
export const attemptSchema = z.object({
  id: z.string(),
  skill: skillSchema,
  score: z.number().min(0).max(100),
  duration: z.number().min(0),
  timestamp: z.number().nonnegative(),
  label: z.string(),
});
export type Attempt = z.infer<typeof attemptSchema>;
export const reviewSchema = z.object({
  id: z.string(),
  ease: z.number().min(1.3),
  interval: z.number().nonnegative(),
  repetitions: z.number().int().nonnegative(),
  due: z.number(),
  introduced: z.number(),
  lastReviewed: z.number(),
  correct: z.number().int().nonnegative(),
  total: z.number().int().nonnegative(),
});
export type Review = z.infer<typeof reviewSchema>;
export const draftSchema = z.object({ id: z.string(), text: z.string(), updated: z.number() });
export type Draft = z.infer<typeof draftSchema>;
export const submissionSchema = z.object({
  id: z.string(),
  promptId: z.string(),
  text: z.string(),
  timestamp: z.number(),
  score: z.number().min(0).max(100),
  feedback: z.array(z.string()),
});
export type Submission = z.infer<typeof submissionSchema>;
export class EnglishDB extends Dexie {
  settings!: Table<Settings, string>;
  attempts!: Table<Attempt, string>;
  words!: Table<Word, string>;
  reviews!: Table<Review, string>;
  drafts!: Table<Draft, string>;
  submissions!: Table<Submission, string>;
  constructor(name = 'englishup') {
    super(name);
    this.version(1).stores({
      settings: 'id',
      attempts: 'id,skill,timestamp',
      words: 'id,word,topic',
      reviews: 'id,due,introduced',
      drafts: 'id',
      submissions: 'id,promptId,timestamp',
    });
  }
}
export const db = new EnglishDB();
export async function logAttempt(skill: Skill, score: number, started: number, label: string) {
  await db.attempts.add({
    id: crypto.randomUUID(),
    skill,
    score: Math.max(0, Math.min(100, score)),
    duration: Math.max(1, Math.round((Date.now() - started) / 1000)),
    timestamp: Date.now(),
    label,
  });
}
export const backupSchema = z.object({
  version: z.literal(1),
  settings: settingsSchema,
  attempts: z.array(attemptSchema),
  words: z.array(wordSchema),
  reviews: z.array(reviewSchema),
  drafts: z.array(draftSchema),
  submissions: z.array(submissionSchema),
});
export async function exportData() {
  return db.transaction('r', db.tables, async () => ({
    version: 1 as const,
    settings: (await db.settings.get('main')) ?? defaults,
    attempts: await db.attempts.toArray(),
    words: await db.words.toArray(),
    reviews: await db.reviews.toArray(),
    drafts: await db.drafts.toArray(),
    submissions: await db.submissions.toArray(),
  }));
}
export async function resetData() {
  await db.transaction('rw', db.tables, async () => {
    for (const table of db.tables) await table.clear();
  });
}
export async function importData(raw: unknown) {
  const data = backupSchema.parse(raw);
  for (const list of [data.attempts, data.words, data.reviews, data.drafts, data.submissions])
    if (new Set(list.map((x) => x.id)).size !== list.length) throw new Error('Duplicate IDs');
  await db.transaction('rw', db.tables, async () => {
    for (const table of db.tables) await table.clear();
    await db.settings.put(data.settings);
    await db.attempts.bulkAdd(data.attempts);
    await db.words.bulkAdd(data.words);
    await db.reviews.bulkAdd(data.reviews);
    await db.drafts.bulkAdd(data.drafts);
    await db.submissions.bulkAdd(data.submissions);
  });
}
export function download(name: string, text: string, type = 'application/json') {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
