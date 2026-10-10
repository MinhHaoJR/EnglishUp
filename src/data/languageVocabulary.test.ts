import { languageVocabulary, languageWordSchema, vocabularyTopics } from './languageVocabulary';

test.each(['ja', 'zh'] as const)(
  '%s provides 2000 distinct complete entries across every topic',
  (language) => {
    const words = languageVocabulary.filter((word) => word.language === language);
    expect(words.length).toBeGreaterThanOrEqual(2000);
    expect(new Set(words.map((word) => word.text.normalize('NFKC'))).size).toBe(words.length);
    expect(new Set(words.map((word) => word.id)).size).toBe(words.length);
    for (const topic of vocabularyTopics)
      expect(words.some((word) => word.topic === topic.id)).toBe(true);
    for (const word of words) {
      expect(languageWordSchema.safeParse(word).success).toBe(true);
      expect(JSON.stringify(word)).not.toContain('\uFFFD');
      expect(word.text).toMatch(/[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u);
      if (language === 'ja')
        expect(word.reading).toMatch(/[\p{Script=Hiragana}\p{Script=Katakana}]/u);
      else expect(word.romanization).toBe(word.reading);
    }
  },
);

test('malformed cross-language IDs and unregistered topics are rejected', () => {
  const word = languageVocabulary[0];
  expect(languageWordSchema.safeParse({ ...word, topic: 'invalid' }).success).toBe(false);
  expect(languageWordSchema.safeParse({ ...word, id: 'invalid' }).success).toBe(false);
  expect(
    languageWordSchema.safeParse({ ...word, language: word.language === 'ja' ? 'zh' : 'ja' })
      .success,
  ).toBe(false);
});
