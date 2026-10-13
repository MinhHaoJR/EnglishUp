import Dexie from 'dexie';
import { vocabulary } from '../data/content';
import { db, EnglishDB, resetData, exportData, importData } from './storage';
import { schedule } from './srs';
import {
  advanceStudyWord,
  beginStudyGroup,
  selectedStudyGroup,
  studyGroups,
  studyScope,
} from './vocabularyStudy';

beforeEach(resetData);
const words = vocabulary.slice(0, 45);
const scope = studyScope('all', 'Daily life');

test('fixed groups cover every word exactly once, including the short last group', () => {
  const groups = studyGroups(words);
  expect(groups.map((group) => group.words.length)).toEqual([20, 20, 5]);
  expect(groups.flatMap((group) => group.words.map((word) => word.id))).toEqual(
    words.map((word) => word.id),
  );
  expect(studyGroups([])).toEqual([]);
});

test('legacy reviews are seeded once and skipping survives reopening without a score', async () => {
  await db.reviews.put(schedule(words[0].id, 'good'));
  const group = studyGroups(words)[0];
  expect((await beginStudyGroup(scope, words, group.id))[0].id).toBe(words[1].id);
  await advanceStudyWord(scope, group.id, words[1], Date.now());
  expect((await beginStudyGroup(scope, words, group.id))[0].id).toBe(words[2].id);
  expect(await db.attempts.count()).toBe(0);
  expect(await db.reviews.get(words[1].id)).toBeUndefined();
  const snapshot = await exportData();
  await resetData();
  await importData(snapshot);
  expect((await beginStudyGroup(scope, words, group.id))[0].id).toBe(words[2].id);
});

test('ratings and progress save atomically and duplicate advancement records only one attempt', async () => {
  await beginStudyGroup(scope, words, words[0].id);
  await Promise.all([
    advanceStudyWord(scope, words[0].id, words[0], Date.now(), 'good'),
    advanceStudyWord(scope, words[0].id, words[0], Date.now(), 'good'),
  ]);
  expect(await db.attempts.count()).toBe(1);
  expect(await db.reviews.get(words[0].id)).toMatchObject({ total: 1 });
  const put = vi.spyOn(db.vocabularyStudy, 'put').mockRejectedValueOnce(new Error('full storage'));
  await expect(
    advanceStudyWord(scope, words[0].id, words[1], Date.now(), 'good'),
  ).rejects.toThrow();
  put.mockRestore();
  expect(await db.reviews.get(words[1].id)).toBeUndefined();
  expect(await db.attempts.count()).toBe(1);
  expect((await beginStudyGroup(scope, words, words[0].id))[0].id).toBe(words[1].id);
});

test('all groups can be studied on the same day, and only explicit replay resets their traversal', async () => {
  for (const group of studyGroups(words)) {
    expect(await beginStudyGroup(scope, words, group.id)).toHaveLength(group.words.length);
    for (const word of group.words)
      await advanceStudyWord(scope, group.id, word, Date.now(), 'again');
    expect(await beginStudyGroup(scope, words, group.id)).toEqual([]);
  }
  expect(await db.attempts.count()).toBe(45);
  const first = studyGroups(words)[0];
  expect(await beginStudyGroup(scope, words, first.id, true)).toHaveLength(20);
  expect(await db.attempts.count()).toBe(45);
  expect((await db.vocabularyStudy.get(scope))?.visitedIds).toHaveLength(25);
});

test('the chosen group resumes independently for each topic and removed group anchors recover', async () => {
  const second = studyGroups(words)[1];
  await beginStudyGroup(scope, words, second.id);
  await advanceStudyWord(scope, second.id, second.words[0], Date.now());
  const progress = await db.vocabularyStudy.get(scope);
  expect(selectedStudyGroup(words, progress, [])?.id).toBe(second.id);
  const otherScope = studyScope('A1', 'Food');
  expect(await db.vocabularyStudy.get(otherScope)).toBeUndefined();
  expect(selectedStudyGroup(words.slice(0, 20), progress, [])?.id).toBe(words[0].id);
});

test('old backups import with empty study progress and invalid progress is rejected before replacement', async () => {
  await beginStudyGroup(scope, words, words[0].id);
  const snapshot = await exportData();
  await expect(
    importData({
      ...snapshot,
      vocabularyStudy: [{ ...snapshot.vocabularyStudy[0], visitedIds: ['x', 'x'] }],
    }),
  ).rejects.toThrow();
  expect(await exportData()).toEqual(snapshot);
  const { vocabularyStudy: removed, ...legacy } = snapshot;
  expect(removed).toHaveLength(1);
  await importData(legacy);
  expect(await db.vocabularyStudy.count()).toBe(0);
});

test('upgrading a version-one database preserves existing learning data', async () => {
  const name = `study-upgrade-${crypto.randomUUID()}`;
  const old = new Dexie(name);
  old.version(1).stores({
    settings: 'id',
    attempts: 'id,skill,timestamp',
    words: 'id,word,topic',
    reviews: 'id,due,introduced',
    drafts: 'id',
    submissions: 'id,promptId,timestamp',
  });
  await old.table('words').put({ ...words[0], custom: true });
  old.close();
  const upgraded = new EnglishDB(name);
  try {
    expect(await upgraded.words.get(words[0].id)).toMatchObject({ word: words[0].word });
    expect(await upgraded.vocabularyStudy.count()).toBe(0);
  } finally {
    await upgraded.delete();
  }
});
