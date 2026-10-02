import {
  matchesTranslation,
  translationSession,
  translationSides,
  wordTranslation,
} from './translation';
import { translations, vocabulary } from '../data/content';

test('matching normalizes Unicode and punctuation but preserves Vietnamese accents', () => {
  expect(matchesTranslation('  TÔI học mỗi ngày! ', ['Tôi học mỗi ngày.'])).toBe(true);
  expect(matchesTranslation('Tôi'.normalize('NFD'), ['Tôi'])).toBe(true);
  expect(matchesTranslation('toi', ['tôi'])).toBe(false);
  expect(matchesTranslation('wrong', ['correct'])).toBe(false);
  expect(matchesTranslation(' ... ', ['anything'])).toBe(false);
});
test('words accept listed meanings and reverse correctly', () => {
  const item = wordTranslation({ ...vocabulary[0], meaning: 'thói quen; tập quán' });
  expect(translationSides(item, 'vi-en').answers).toEqual([vocabulary[0].word]);
  expect(matchesTranslation('tập quán', translationSides(item, 'en-vi').answers)).toBe(true);
});
test('random sessions cover valid content without modifying the source', () => {
  expect(new Set(translations.map((item) => item.topic)).size).toBe(8);
  const before = translations.map((item) => item.id);
  const session = translationSession(translations);
  expect(session).toHaveLength(10);
  expect(new Set(session.map((item) => item.id)).size).toBe(10);
  expect(translations.map((item) => item.id)).toEqual(before);
  expect(translationSession([])).toEqual([]);
});
