import type { Word, Level } from '../data/schema';
import { db, logAttempt, type Review, type VocabularyStudy } from './storage';
import { schedule, type Rating } from './srs';

export const STUDY_GROUP_SIZE = 20;
export function studyScope(level: Level | 'all', topic: string) {
  return JSON.stringify(['en', level, topic]);
}
export function studyGroups(words: Word[]) {
  return Array.from({ length: Math.ceil(words.length / STUDY_GROUP_SIZE) }, (_, index) => {
    const entries = words.slice(index * STUDY_GROUP_SIZE, (index + 1) * STUDY_GROUP_SIZE);
    return { id: entries[0].id, number: index + 1, words: entries };
  });
}
export function visitedWords(
  words: Word[],
  progress: VocabularyStudy | undefined,
  reviews: Review[],
) {
  // Import previous learning on first use; explicit replays then use the saved traversal.
  return new Set(
    progress?.visitedIds ??
      words
        .filter((word) => reviews.some((review) => review.id === word.id))
        .map((word) => word.id),
  );
}
export function selectedStudyGroup(
  words: Word[],
  progress: VocabularyStudy | undefined,
  reviews: Review[],
) {
  const groups = studyGroups(words);
  const visited = visitedWords(words, progress, reviews);
  return (
    groups.find((group) => group.id === progress?.selectedGroupId) ??
    groups.find((group) => group.words.some((word) => !visited.has(word.id))) ??
    groups[0]
  );
}

/** A fixed group is resumed in catalog order, independent of the daily SRS due queue. */
export async function beginStudyGroup(
  scope: string,
  words: Word[],
  groupId: string,
  replay = false,
) {
  const group = studyGroups(words).find((item) => item.id === groupId);
  if (!group) throw new Error('Unknown vocabulary group');
  return db.transaction('rw', db.vocabularyStudy, db.reviews, async () => {
    const previous = await db.vocabularyStudy.get(scope);
    const visited = visitedWords(words, previous, await db.reviews.toArray());
    if (replay) group.words.forEach((word) => visited.delete(word.id));
    await db.vocabularyStudy.put({
      id: scope,
      selectedGroupId: groupId,
      visitedIds: [...visited],
      updated: Date.now(),
    });
    return group.words.filter((word) => !visited.has(word.id));
  });
}

export async function selectStudyGroup(scope: string, words: Word[], groupId: string) {
  await beginStudyGroup(scope, words, groupId);
}

/** Rating + progress + attempt commit together; skipping changes traversal only. */
export async function advanceStudyWord(
  scope: string,
  groupId: string,
  word: Word,
  started: number,
  rating?: Rating,
) {
  await db.transaction('rw', db.vocabularyStudy, db.reviews, db.attempts, async () => {
    const progress = await db.vocabularyStudy.get(scope);
    if (!progress || progress.selectedGroupId !== groupId)
      throw new Error('Study selection changed; reopen this group');
    if (progress.visitedIds.includes(word.id)) return;
    if (rating) {
      const previous = await db.reviews.get(word.id);
      await db.reviews.put(schedule(word.id, rating, previous));
      await logAttempt(
        'vocabulary',
        { again: 0, hard: 60, good: 85, easy: 100 }[rating],
        started,
        word.word,
        'en',
      );
    }
    await db.vocabularyStudy.put({
      ...progress,
      visitedIds: [...progress.visitedIds, word.id],
      updated: Date.now(),
    });
  });
}
