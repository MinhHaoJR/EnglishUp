import { z } from 'zod';
import raw from './language-vocabulary.json';

export const vocabularyTopics = [
  { id: 'greetings', vi: 'Giao tiếp hằng ngày', en: 'Everyday expressions', mark: '↗' },
  { id: 'people', vi: 'Con người & gia đình', en: 'People & family', mark: '人' },
  { id: 'home', vi: 'Nhà cửa', en: 'At home', mark: '⌂' },
  { id: 'food', vi: 'Đồ ăn', en: 'Food', mark: '食' },
  { id: 'drinks', vi: 'Đồ uống & hương vị', en: 'Drinks & flavors', mark: '茶' },
  { id: 'shopping', vi: 'Mua sắm', en: 'Shopping', mark: '＋' },
  { id: 'travel', vi: 'Du lịch', en: 'Travel', mark: '↗' },
  { id: 'transport', vi: 'Đi lại', en: 'Transport', mark: '→' },
  { id: 'time', vi: 'Thời gian', en: 'Time', mark: '日' },
  { id: 'nature', vi: 'Thiên nhiên', en: 'Nature', mark: '山' },
  { id: 'animals', vi: 'Động vật', en: 'Animals', mark: '鳥' },
  { id: 'body', vi: 'Cơ thể', en: 'The body', mark: '手' },
  { id: 'health', vi: 'Sức khỏe', en: 'Health', mark: '＋' },
  { id: 'school', vi: 'Học tập', en: 'Learning', mark: '学' },
  { id: 'work', vi: 'Công việc', en: 'Work', mark: '▧' },
  { id: 'technology', vi: 'Công nghệ', en: 'Technology', mark: '⌘' },
  { id: 'activities', vi: 'Hoạt động & sở thích', en: 'Activities & hobbies', mark: '♪' },
  { id: 'verbs', vi: 'Động từ', en: 'Verbs', mark: '↔' },
  { id: 'adjectives', vi: 'Tính chất & cảm xúc', en: 'Qualities & feelings', mark: '◇' },
  { id: 'society', vi: 'Đời sống & xã hội', en: 'Life & society', mark: '世' },
] as const;

export const languageWordSchema = z
  .object({
    id: z.string().regex(/^(ja|zh)-vocab-\d{4}$/),
    language: z.enum(['ja', 'zh']),
    text: z.string().trim().min(1),
    reading: z.string().trim().min(1),
    romanization: z.string().trim().min(1),
    meaning: z.object({ vi: z.string().trim().min(1), en: z.string().trim().min(1) }),
    topic: z.string().refine((value) => vocabularyTopics.some((topic) => topic.id === value)),
  })
  .refine((word) => word.id.startsWith(`${word.language}-`), 'ID must match language');

export type LanguageWord = z.infer<typeof languageWordSchema>;
export type VocabularyLanguage = LanguageWord['language'];
export const languageVocabulary = z
  .array(languageWordSchema)
  .superRefine((words, ctx) => {
    for (const key of ['id', 'text'] as const) {
      const values = words.map((word) => `${word.language}:${word[key].normalize('NFKC')}`);
      if (new Set(values).size !== values.length)
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: `Duplicate vocabulary ${key}` });
    }
  })
  .parse(raw);
