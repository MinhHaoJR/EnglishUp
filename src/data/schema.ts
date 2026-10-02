import { z } from 'zod';
export const levelSchema = z.enum(['A1', 'A2', 'B1', 'B2', 'C1']);
export const skillSchema = z.enum(['vocabulary', 'listening', 'speaking', 'reading', 'writing']);
export const wordSchema = z.object({
  id: z.string().min(1),
  word: z.string().trim().min(1),
  ipa: z.string(),
  pos: z.string().trim().min(1),
  meaning: z.string().trim().min(1),
  definition: z.string().trim().min(1),
  examples: z.array(z.string().trim().min(1)).min(1).max(2),
  level: levelSchema,
  topic: z.string().trim().min(1),
  custom: z.boolean().optional(),
});
export type Word = z.infer<typeof wordSchema>;
export type Skill = z.infer<typeof skillSchema>;
export type Level = z.infer<typeof levelSchema>;
export const questionSchema = z
  .object({
    id: z.string(),
    type: z.enum(['choice', 'tfng', 'short', 'blank']),
    prompt: z.string(),
    options: z.array(z.string()).optional(),
    answers: z.array(z.string()).min(1),
    explanation: z.string(),
    evidence: z.string(),
  })
  .superRefine((q, ctx) => {
    if (
      q.type === 'choice' &&
      (!q.options || q.options.length < 2 || q.answers.some((a) => !q.options?.includes(a)))
    )
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Choice questions need at least two options containing every accepted answer',
      });
    if (q.type === 'tfng' && q.answers.some((a) => !['True', 'False', 'Not Given'].includes(a)))
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: 'Invalid True/False/Not Given answer' });
  });
export type Question = z.infer<typeof questionSchema>;
export const readingSchema = z.object({
  id: z.string(),
  title: z.string(),
  level: levelSchema,
  topic: z.string(),
  text: z.string(),
  questions: z.array(questionSchema).length(5),
});
export type ReadingLesson = z.infer<typeof readingSchema>;
export const listeningSchema = z.object({
  id: z.string(),
  title: z.string(),
  level: levelSchema,
  topic: z.string(),
  lines: z.array(z.object({ speaker: z.string(), text: z.string() })).min(1),
  questions: z.array(questionSchema).min(4).max(5),
});
export type ListeningLesson = z.infer<typeof listeningSchema>;
export const dictationSchema = z.object({
  id: z.string(),
  text: z.string(),
  level: levelSchema,
  topic: z.string(),
});
export const speakingSchema = z.object({
  id: z.string(),
  title: z.string(),
  level: levelSchema,
  topic: z.string(),
  mode: z.enum(['read', 'talk']),
  text: z.string(),
  cues: z.array(z.string()).min(1),
});
export type SpeakingPrompt = z.infer<typeof speakingSchema>;
export const writingSchema = z
  .object({
    id: z.string(),
    title: z.string(),
    level: levelSchema,
    topic: z.string(),
    genre: z.enum(['email', 'opinion', 'description', 'story']),
    prompt: z.string(),
    minWords: z.number().int().positive(),
    maxWords: z.number().int().positive(),
    checklist: z.array(z.string()).min(3),
  })
  .refine((p) => p.maxWords >= p.minWords, 'Invalid word range');
export type WritingPrompt = z.infer<typeof writingSchema>;
