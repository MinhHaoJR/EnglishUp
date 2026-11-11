import { z } from 'zod';
export const levelSchema = z.enum(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']);
export const skillSchema = z.enum([
  'vocabulary',
  'listening',
  'speaking',
  'reading',
  'writing',
  'grammar',
]);
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
  /** Last edit of a custom word; orders account sync. */
  updated: z.number().nonnegative().optional(),
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
export type Dictation = z.infer<typeof dictationSchema>;
export const translationSchema = z.object({
  id: z.string().min(1),
  level: levelSchema,
  topic: z.string().min(1),
  en: z.array(z.string().trim().min(1)).min(1),
  vi: z.array(z.string().trim().min(1)).min(1),
});
export type Translation = z.infer<typeof translationSchema>;

/** Grammar points the fill-in-the-blank questions practise, with their Vietnamese and English names. */
export const quizCategories = {
  tense: ['Thì động từ', 'Tenses'],
  article: ['Mạo từ', 'Articles'],
  preposition: ['Giới từ', 'Prepositions'],
  adverb: ['Trạng từ', 'Adverbs'],
  comparison: ['So sánh', 'Comparison'],
  conditional: ['Câu điều kiện và câu ước', 'Conditionals and wishes'],
  passive: ['Câu bị động', 'The passive'],
  modal: ['Động từ khuyết thiếu', 'Modal verbs'],
  verbform: ['Dạng động từ (to-V, V-ing)', 'Verb forms (to-V, V-ing)'],
  connector: ['Liên từ và từ nối', 'Linking words'],
  relative: ['Mệnh đề quan hệ', 'Relative clauses'],
  quantifier: ['Từ chỉ lượng', 'Quantifiers'],
  pronoun: ['Đại từ', 'Pronouns'],
  reported: ['Câu tường thuật', 'Reported speech'],
  inversion: ['Đảo ngữ', 'Inversion'],
} as const satisfies Record<string, readonly [string, string]>;
export type QuizCategory = keyof typeof quizCategories;
/** One sentence with a single blank (___) and four options, exactly one of them right. */
export const quizSchema = z
  .object({
    id: z.string().min(1),
    level: levelSchema,
    category: z.enum(Object.keys(quizCategories) as [QuizCategory, ...QuizCategory[]]),
    sentence: z.string().trim().min(1),
    options: z.array(z.string().trim().min(1)).length(4),
    answer: z.string().trim().min(1),
    explanation: z.string().trim().min(1),
  })
  .refine((q) => q.sentence.split('___').length === 2, 'The sentence needs exactly one blank (___)')
  .refine((q) => new Set(q.options).size === 4, 'The four options must differ')
  .refine((q) => q.options.includes(q.answer), 'The answer must be one of the options');
export type Quiz = z.infer<typeof quizSchema>;

const bilingualText = z.object({ vi: z.string().trim().min(1), en: z.string().trim().min(1) });
/** One English tense: its form, uses with examples, signal words, a tip and three quick checks. */
export const tenseSchema = z.object({
  id: z.string().regex(/^t-[a-z-]+$/),
  order: z.number().int().min(1),
  group: z.enum(['past', 'present', 'future']),
  level: levelSchema,
  name: bilingualText,
  forms: z.object({
    affirmative: z.array(z.string().trim().min(1)).min(1),
    negative: z.array(z.string().trim().min(1)).min(1),
    question: z.array(z.string().trim().min(1)).min(1),
  }),
  uses: z
    .array(
      z.object({
        vi: z.string().trim().min(1),
        en: z.string().trim().min(1),
        example: z.string().trim().min(1),
      }),
    )
    .min(1),
  signals: z.array(z.string().trim().min(1)).min(1),
  tip: bilingualText,
  practice: z
    .array(
      z
        .object({
          sentence: z.string().trim().min(1),
          options: z.array(z.string().trim().min(1)).length(4),
          answer: z.string().trim().min(1),
          explanation: z.string().trim().min(1),
        })
        .refine(
          (q) => q.sentence.split('___').length === 2,
          'The sentence needs exactly one blank (___)',
        )
        .refine((q) => new Set(q.options).size === 4, 'The four options must differ')
        .refine((q) => q.options.includes(q.answer), 'The answer must be one of the options'),
    )
    .min(1),
});
export type Tense = z.infer<typeof tenseSchema>;

export const guideCategories = {
  greeting: ['Chào hỏi', 'Greetings'],
  about: ['Giới thiệu EnglishUp', 'About EnglishUp'],
  placement: ['Kiểm tra trình độ', 'Level test'],
  roadmap: ['Lộ trình học', 'Learning paths'],
  practice: ['Cách luyện tập', 'How to practise'],
  account: ['Tài khoản và học tập', 'Account and study'],
} as const satisfies Record<string, readonly [string, string]>;
/** One answer the AI tutor gives about EnglishUp itself: greetings, the app, the level test, the paths. */
export const guideSchema = z.object({
  id: z.string().regex(/^g-[a-z0-9-]+$/),
  category: z.enum(Object.keys(guideCategories) as [keyof typeof guideCategories]),
  question: bilingualText,
  answer: bilingualText,
  keywords: z.array(z.string().trim().min(1)).default([]),
});
export type Guide = z.infer<typeof guideSchema>;

/** Where a learning-path task sends the learner: a practice page, a game, the tutor or the level test. */
export const roadmapSkills = [
  'vocabulary',
  'translation',
  'relations',
  'grammar',
  'reading',
  'listening',
  'speaking',
  'writing',
  'wordgame',
  'grammargame',
  'tenses',
  'assistant',
  'placement',
] as const;
export type RoadmapSkill = (typeof roadmapSkills)[number];
/** Names of the pages a learning-path task can open. */
export const roadmapSkillLabels: Record<RoadmapSkill, [string, string]> = {
  vocabulary: ['Từ vựng', 'Vocabulary'],
  translation: ['Luyện dịch', 'Translation'],
  relations: ['Đồng nghĩa – trái nghĩa', 'Synonyms & antonyms'],
  grammar: ['Cấu trúc câu', 'Sentence patterns'],
  reading: ['Luyện đọc', 'Reading'],
  listening: ['Luyện nghe', 'Listening'],
  speaking: ['Luyện nói', 'Speaking'],
  writing: ['Luyện viết', 'Writing'],
  wordgame: ['Đua từ vựng', 'Vocabulary race'],
  grammargame: ['Đua ngữ pháp', 'Grammar race'],
  tenses: ['Các thì', 'Tenses'],
  assistant: ['Trợ giảng AI', 'AI tutor'],
  placement: ['Kiểm tra trình độ', 'Level test'],
};
const bilingual = z.object({ vi: z.string().trim().min(1), en: z.string().trim().min(1) });
/** A learning path from one level to the next: stages with a goal, each with practice tasks. */
export const roadmapSchema = z
  .object({
    id: z.string().regex(/^rm-(a1|a2|b1|b2|c1)-(a2|b1|b2|c1|c2)$/),
    from: levelSchema,
    to: levelSchema,
    weeks: z.number().int().min(1).max(52),
    title: bilingual,
    summary: bilingual,
    stages: z
      .array(
        z.object({
          id: z.string().min(1),
          title: bilingual,
          goal: bilingual,
          tasks: z
            .array(
              z.object({
                id: z.string().min(1),
                skill: z.enum(roadmapSkills),
                level: levelSchema,
                /** A quiz category for a grammar race; empty means every grammar point. */
                category: z.string().optional(),
                vi: z.string().trim().min(1),
                en: z.string().trim().min(1),
              }),
            )
            .min(1),
        }),
      )
      .min(1),
  })
  .refine(
    (r) => levelSchema.options.indexOf(r.to) === levelSchema.options.indexOf(r.from) + 1,
    'A path goes from one level to the next',
  )
  .refine(
    (r) =>
      new Set(r.stages.flatMap((s) => s.tasks.map((t) => t.id))).size ===
      r.stages.flatMap((s) => s.tasks).length,
    'Task ids must differ',
  );
export type Roadmap = z.infer<typeof roadmapSchema>;
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

export const structureGroups = [
  'linking',
  'degree',
  'to-v',
  'v-ing',
  'sb-do',
  'change',
  'ing-phrases',
  'habits',
  'compare',
  'time',
  'it-there',
  'academic',
] as const;
/** A sentence pattern with an original example; `key` is the part of the example the quiz blanks out. */
export const structureSchema = z
  .object({
    id: z.string().regex(/^s\d{3}$/),
    group: z.enum(structureGroups),
    formula: z.string().trim().min(1),
    meaning: z.string().trim().min(1),
    example: z.string().trim().min(1),
    key: z.string().trim().min(1),
    options: z.array(z.string().trim().min(1)).length(2),
    translation: z.string().trim().min(1),
  })
  .refine(
    (s) => s.example.split(s.key).length === 2,
    'The key must appear exactly once in the example',
  )
  .refine(
    (s) => new Set([s.key, ...s.options]).size === 3,
    'Wrong options must differ from each other and from the key',
  );
export type Structure = z.infer<typeof structureSchema>;
export type StructureGroup = (typeof structureGroups)[number];
