import {
  filterLanguageWords,
  normalizeVocabularySearch,
  vocabularyPractice,
  saveWordPractice,
  meaningsOverlap,
} from './languageVocabulary';
import { db, exportData, importData, resetData } from './storage';
import type { LanguageWord } from '../data/languageVocabulary';

const word: LanguageWord = {
  id: 'zh-vocab-0001',
  language: 'zh',
  text: '你好',
  reading: 'nǐ hǎo',
  romanization: 'nǐ hǎo',
  meaning: { vi: 'xin chào', en: 'hello' },
  topic: 'greetings',
};
const japanese: LanguageWord = {
  ...word,
  id: 'ja-vocab-0001',
  language: 'ja',
  text: '学校',
  reading: 'がっこう',
  romanization: 'gakkō',
  meaning: { vi: 'trường học', en: 'school' },
  topic: 'school',
};

test('search accepts scripts, kana, romaji, toneless pinyin and accent-free Vietnamese', () => {
  for (const query of ['你好', 'ni hao', 'NIHAO', 'xin chao'])
    expect(filterLanguageWords([word], 'all', query)).toEqual([word]);
  for (const query of ['学校', 'がっこう', 'gakko', 'truong hoc'])
    expect(filterLanguageWords([japanese], 'school', query)).toEqual([japanese]);
  expect(filterLanguageWords([word, japanese], 'school', 'hello')).toEqual([]);
  expect(normalizeVocabularySearch('ば')).not.toBe(normalizeVocabularySearch('は'));
});

test('practice uses the selected words, varied options and the same language only', () => {
  const catalog = [
    word,
    japanese,
    ...Array.from({ length: 12 }, (_, i) => ({
      ...word,
      id: `zh-vocab-${String(i + 2).padStart(4, '0')}`,
      text: `word ${i}`,
      meaning: { vi: `nghĩa ${i}`, en: `meaning ${i}` },
    })),
  ];
  const first = catalog[5];
  const questions = vocabularyPractice(
    catalog.filter((w) => w.language === 'zh'),
    catalog,
    first,
    () => 0.4,
  );
  expect(questions).toHaveLength(10);
  expect(questions[0].word).toEqual(first);
  expect(new Set(questions.map((q) => q.word.id)).size).toBe(10);
  for (const question of questions) {
    expect(question.options).toHaveLength(4);
    expect(question.options).toContain(question.word);
    expect(question.options.every((option) => option.language === 'zh')).toBe(true);
    expect(new Set(question.options.map((option) => option.meaning.vi)).size).toBe(4);
  }
  expect(vocabularyPractice([], catalog)).toEqual([]);
});

test('language vocabulary results persist independently and survive backup/reset/import', async () => {
  await resetData();
  await saveWordPractice(word, true, Date.now());
  await saveWordPractice(japanese, false, Date.now());
  const saved = await db.attempts.toArray();
  expect(saved).toHaveLength(2);
  expect(saved).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        skill: 'vocabulary',
        learningLanguage: 'zh',
        label: '你好',
        score: 100,
      }),
      expect.objectContaining({
        skill: 'vocabulary',
        learningLanguage: 'ja',
        label: '学校',
        score: 0,
      }),
    ]),
  );
  const backup = await exportData();
  await resetData();
  await importData(backup);
  expect(await exportData()).toEqual(backup);
});

test('quiz excludes alternatives sharing any listed translation', () => {
  const first = { ...word, meaning: { vi: 'xin lỗi; làm phiền', en: 'sorry; excuse me' } };
  const same = { ...word, id: 'zh-vocab-0002', meaning: { vi: 'xin lỗi', en: 'sorry' } };
  const other = { ...word, id: 'zh-vocab-0003', meaning: { vi: 'cảm ơn', en: 'thank you' } };
  expect(meaningsOverlap(first, same)).toBe(true);
  expect(meaningsOverlap(first, other)).toBe(false);
  const question = vocabularyPractice([first], [first, same, other], first)[0];
  expect(question.options.map((option) => option.id)).not.toContain(same.id);
  expect(question.options).toContain(other);
});
