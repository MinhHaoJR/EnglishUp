import type {
  Dictation,
  Quiz,
  Roadmap,
  Tense,
  Guide,
  ListeningLesson,
  ReadingLesson,
  SpeakingPrompt,
  Structure,
  Translation,
  Word,
  WritingPrompt,
} from './schema';

/*
 * The English learning library. It lives in the server's database (Supabase); services/content.ts fills these
 * lists in place from GET /api/content, or from the offline copy in Dexie, before any page renders.
 * The JSON files beside this module are seed data only: the server's `seed` command and the tests read them.
 */
export const vocabulary: Word[] = [];
export const structures: Structure[] = [];
export const readings: ReadingLesson[] = [];
export const listenings: ListeningLesson[] = [];
export const dictations: Dictation[] = [];
export const speakingPrompts: SpeakingPrompt[] = [];
export const writingPrompts: WritingPrompt[] = [];
export const translations: Translation[] = [];
export const quizzes: Quiz[] = [];
export const roadmaps: Roadmap[] = [];
export const tenses: Tense[] = [];
export const guides: Guide[] = [];
