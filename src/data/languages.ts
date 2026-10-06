import { z } from 'zod';
import raw from './languages.json';
const bilingual = z.object({ vi: z.string().min(1), en: z.string().min(1) });
const lessonSchema = z
  .object({
    id: z.string().min(1),
    language: z.enum(['ja', 'zh']),
    title: bilingual,
    text: z.string().min(1),
    romanization: z.string().min(1),
    meaning: bilingual,
    passage: z.string().min(1),
    question: bilingual,
    options: z.array(bilingual).min(2),
    answer: z.number().int().nonnegative(),
  })
  .refine((lesson) => lesson.answer < lesson.options.length, 'Invalid answer');
export const languageLessons = z
  .array(lessonSchema)
  .refine(
    (lessons) => new Set(lessons.map((lesson) => lesson.id)).size === lessons.length,
    'Duplicate lesson IDs',
  )
  .parse(raw);
export type LanguageLesson = z.infer<typeof lessonSchema>;
export const languageNames = {
  en: { vi: 'Tiếng Anh', en: 'English', native: 'English', mark: 'Aa' },
  ja: { vi: 'Tiếng Nhật', en: 'Japanese', native: '日本語', mark: 'あ' },
  zh: { vi: 'Tiếng Trung', en: 'Chinese', native: '中文', mark: '中' },
};
