import { wordRelations, wordRelationSchema } from '../data/wordRelations';
import { levelSchema, wordSchema } from '../data/schema';
import { vocabulary } from '../data/content';
import { createRelationSession, filterRelations, saveRelationAnswer } from './wordRelations';
import { db, resetData, exportData, importData } from './storage';
import { importCSV, exportCSV } from './csv';

beforeEach(resetData);

test('all six lesson levels contain complete, distinct relations and original contextual examples', () => {
  expect(wordRelations).toHaveLength(72);
  expect(new Set(wordRelations.map((entry) => entry.word)).size).toBe(72);
  for (const level of levelSchema.options) {
    expect(wordRelations.filter((entry) => entry.level === level)).toHaveLength(12);
  }
  const examples = wordRelations.flatMap((entry) => [
    entry.example,
    entry.synonyms[0].example,
    entry.antonyms[0].example,
  ]);
  expect(new Set(examples).size).toBe(examples.length);
  for (const entry of wordRelations) {
    expect(entry.example.toLowerCase()).toContain(entry.word.toLowerCase());
    expect(entry.usageNote.vi.length).toBeGreaterThan(20);
    expect(entry.usageNote.en.length).toBeGreaterThan(20);
    expect(JSON.stringify(entry)).not.toContain('\uFFFD');
  }
});

test('schema rejects conflicting answers, missing senses and mislabeled level IDs', () => {
  const entry = wordRelations[0];
  expect(wordRelationSchema.safeParse({ ...entry, antonyms: entry.synonyms }).success).toBe(false);
  expect(wordRelationSchema.safeParse({ ...entry, word: entry.synonyms[0].word }).success).toBe(
    false,
  );
  expect(wordRelationSchema.safeParse({ ...entry, definition: '  ' }).success).toBe(false);
  expect(wordRelationSchema.safeParse({ ...entry, level: 'C2' }).success).toBe(false);
  expect(wordRelationSchema.safeParse({ ...entry, level: 'IELTS 7' }).success).toBe(false);
});

test('search includes related terms and Vietnamese meanings while keeping the selected level', () => {
  const entry = wordRelations.find((item) => item.level === 'C2')!;
  expect(
    filterRelations(wordRelations, 'C2', ` ${entry.synonyms[0].word.toUpperCase()} `),
  ).toContain(entry);
  expect(filterRelations(wordRelations, 'C2', entry.antonyms[0].word)).toContain(entry);
  const plainMeaning = entry.meaning.normalize('NFD').replace(/\p{M}/gu, '').replace(/đ/g, 'd');
  expect(filterRelations(wordRelations, 'C2', plainMeaning)).toContain(entry);
  expect(filterRelations(wordRelations, 'A1', entry.word)).not.toContain(entry);
  expect(filterRelations(wordRelations, 'all', 'no-such-relation-xyz')).toEqual([]);
});

test('practice is bounded, respects the selection and contrasts only the checked relation pair', () => {
  const selection = filterRelations(wordRelations, 'B2', '');
  const originalOrder = selection.map((entry) => entry.id);
  const queue = createRelationSession(selection, 'mixed', 100, () => 0.35);
  expect(queue).toHaveLength(10);
  expect(new Set(queue.map((question) => question.entry.id)).size).toBe(10);
  expect(new Set(queue.map((question) => question.kind))).toEqual(new Set(['synonym', 'antonym']));
  for (const question of queue) {
    expect(question.entry.level).toBe('B2');
    expect(question.options).toHaveLength(2);
    expect(new Set(question.options).size).toBe(2);
    expect(question.options).toContain(question.answer);
    expect(question.answer).toBe(
      (question.kind === 'synonym' ? question.entry.synonyms : question.entry.antonyms)[0].word,
    );
  }
  expect(selection.map((entry) => entry.id)).toEqual(originalOrder);
  expect(createRelationSession([], 'mixed')).toEqual([]);
  expect(createRelationSession(selection, 'mixed', 0)).toEqual([]);
  expect(
    createRelationSession(selection, 'antonym', 2).every((question) => question.kind === 'antonym'),
  ).toBe(true);
  expect(createRelationSession(selection.slice(0, 1), 'synonym')).toHaveLength(1);
});

test('correct and incorrect answers persist with English history and survive backup alongside C2 words', async () => {
  const question = createRelationSession(
    wordRelations.filter((entry) => entry.level === 'C2'),
    'synonym',
    1,
  )[0];
  await expect(saveRelationAnswer(question, '', Date.now())).rejects.toThrow();
  await expect(saveRelationAnswer(question, 'not-an-option', Date.now())).rejects.toThrow();
  expect(await db.attempts.count()).toBe(0);
  await saveRelationAnswer(question, question.answer, Date.now() - 3000);
  await saveRelationAnswer(
    question,
    question.options.find((option) => option !== question.answer)!,
    Date.now(),
  );
  const attempts = await db.attempts.toArray();
  expect(attempts.map((attempt) => attempt.score).sort((a, b) => a - b)).toEqual([0, 100]);
  for (const attempt of attempts) {
    expect(attempt).toMatchObject({ skill: 'vocabulary', learningLanguage: 'en' });
    expect(attempt.label).toContain(`C2: ${question.entry.word}`);
  }
  expect(await db.reviews.count()).toBe(0);
  const custom = wordSchema.parse({ ...vocabulary[0], id: 'c2-custom', level: 'C2', custom: true });
  expect(importCSV(exportCSV([custom]))[0].level).toBe('C2');
  await db.words.put(custom);
  const backup = await exportData();
  await resetData();
  await importData(backup);
  expect(await exportData()).toEqual(backup);
});
