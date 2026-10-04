import {
  vocabulary,
  readings,
  listenings,
  dictations,
  speakingPrompts,
  writingPrompts,
} from './content';
import { wordSchema, questionSchema } from './schema';
import { topics, topicVi } from '../i18n';
test('expanded catalog has translated topics, complete IT entries and stable original IDs', () => {
  expect(vocabulary).toHaveLength(240);
  expect(new Set(vocabulary.map((word) => word.topic)).size).toBe(16);
  for (const topic of topics) {
    expect(topicVi[topic]).toBeTruthy();
    expect(vocabulary.some((word) => word.topic === topic)).toBe(true);
  }
  const itTopics = topics.filter((topic) => topic.startsWith('IT:'));
  expect(itTopics).toHaveLength(6);
  for (const topic of itTopics) {
    const words = vocabulary.filter((word) => word.topic === topic);
    expect(words).toHaveLength(10);
    for (const word of words) {
      expect(word.ipa).toMatch(/^\/.+\/$/);
      expect(word.examples[0].toLowerCase()).toContain(word.word.toLowerCase());
    }
  }
  expect(vocabulary.find((word) => word.id === 'v-1-1')?.word).toBe('routine');
  expect(vocabulary.filter((word) => /^v-\d+-\d+$/.test(word.id))).toHaveLength(160);
});
test('original vocabulary meets quantity, topic and schema requirements', () => {
  expect(vocabulary.length).toBeGreaterThanOrEqual(150);
  expect(new Set(vocabulary.map((w) => w.topic)).size).toBeGreaterThanOrEqual(8);
  expect(new Set(vocabulary.map((w) => w.word)).size).toBe(vocabulary.length);
  expect(vocabulary.every((w) => ['A2', 'B1', 'B2'].includes(w.level))).toBe(true);
});
test('all original content meets counts and has unique IDs and valid answer choices', () => {
  expect(listenings.length).toBeGreaterThanOrEqual(6);
  expect(dictations.length).toBeGreaterThanOrEqual(10);
  expect(speakingPrompts.filter((p) => p.mode === 'read').length).toBeGreaterThanOrEqual(8);
  expect(speakingPrompts.filter((p) => p.mode === 'talk').length).toBeGreaterThanOrEqual(8);
  expect(writingPrompts.length).toBeGreaterThanOrEqual(10);
  for (const list of [
    vocabulary,
    readings,
    listenings,
    dictations,
    speakingPrompts,
    writingPrompts,
  ])
    expect(new Set(list.map((x) => x.id)).size).toBe(list.length);
  for (const lesson of [...readings, ...listenings])
    for (const q of lesson.questions) {
      if (q.type === 'choice') expect(q.options).toEqual(expect.arrayContaining(q.answers));
      if (q.type === 'tfng') expect(['True', 'False', 'Not Given']).toContain(q.answers[0]);
    }
  for (const lesson of listenings)
    for (const q of lesson.questions)
      expect(lesson.lines.map((l) => l.text).join(' ')).toContain(q.evidence);
  expect(wordSchema.safeParse({ ...vocabulary[0], level: 'D2' }).success).toBe(false);
  expect(questionSchema.safeParse({ id: 'bad' }).success).toBe(false);
});
test('reading passages have 150–350 words, five questions and exact evidence', () => {
  expect(readings.length).toBeGreaterThanOrEqual(6);
  for (const r of readings) {
    const count = r.text.split(/\s+/).length;
    expect(count).toBeGreaterThanOrEqual(150);
    expect(count).toBeLessThanOrEqual(350);
    expect(r.questions).toHaveLength(5);
    for (const q of r.questions) expect(r.text).toContain(q.evidence);
  }
});
