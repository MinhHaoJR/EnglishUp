import {
  vocabulary,
  readings,
  listenings,
  dictations,
  speakingPrompts,
  writingPrompts,
} from './content';
import { wordSchema, questionSchema } from './schema';
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
