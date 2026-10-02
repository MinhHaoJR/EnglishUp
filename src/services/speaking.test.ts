import { speakingMetrics } from './speaking';
test('topic metrics count words, filler phrases and variety', () => {
  const result = speakingMetrics('Um I like tea you know I like tea', 30);
  expect(result.words).toBe(9);
  expect(result.wpm).toBe(18);
  expect(result.fillers).toBe(4);
  expect(result.variety).toBe(67);
});
