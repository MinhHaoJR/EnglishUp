import { alignWords, normalize } from './diff';
test('normalizes punctuation, case and common contractions', () => {
  expect(normalize("I'm ready, but we shouldn’t rush!")).toEqual([
    'i',
    'am',
    'ready',
    'but',
    'we',
    'should',
    'not',
    'rush',
  ]);
  expect(alignWords('I am here.', 'I’m here').score).toBe(100);
});
test('aligns missing, wrong and extra words', () => {
  expect(
    alignWords('we eat fresh rice', 'we eat rice').tokens.some(
      (t) => t.kind === 'missing' && t.expected === 'fresh',
    ),
  ).toBe(true);
  expect(alignWords('we eat rice', 'we eat nice rice').tokens.some((t) => t.kind === 'extra')).toBe(
    true,
  );
  expect(alignWords('we eat rice', 'we eat bread').score).toBe(67);
  expect(alignWords('one two', '').score).toBe(0);
  expect(alignWords('one', 'one two three four').score).toBe(0);
  expect(alignWords('', '').score).toBe(100);
});
test('dictation gives exact score for one omission', () => {
  expect(alignWords('Please bring a small bag.', 'please bring a bag').score).toBe(80);
});
