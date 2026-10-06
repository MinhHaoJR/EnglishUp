import type { Skill } from '../data/schema';
import type { LanguageLesson } from '../data/languages';
import { db, logAttempt } from './storage';
export function matchesModel(answer: string, model: string) {
  const normalize = (text: string) => text.normalize('NFKC').replace(/[\s。、，.!！?？]/gu, '');
  return normalize(answer) === normalize(model);
}
export async function saveLanguagePractice(
  lesson: LanguageLesson,
  skill: Skill,
  score: number,
  started: number,
  text: string,
) {
  await db.transaction('rw', db.attempts, db.submissions, async () => {
    await logAttempt(
      skill,
      score,
      started,
      `${lesson.text}${skill === 'speaking' ? ' · self-assessed' : ''}`,
      lesson.language,
    );
    if (skill === 'writing')
      await db.submissions.add({
        id: crypto.randomUUID(),
        promptId: lesson.id,
        text,
        timestamp: Date.now(),
        score,
        feedback: ['Model comparison only'],
      });
  });
}
