import type { LanguageWord } from '../data/languageVocabulary';
import { logAttempt } from './storage';

export function normalizeVocabularySearch(value: string) {
  return value
    .normalize('NFKC')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .normalize('NFC')
    .toLocaleLowerCase()
    .replace(/đ/g, 'd')
    .replace(/\s+/g, '');
}

export function filterLanguageWords(words: LanguageWord[], topic: string, search: string) {
  const query = normalizeVocabularySearch(search);
  return words.filter(
    (word) =>
      (topic === 'all' || word.topic === topic) &&
      [word.text, word.reading, word.romanization, word.meaning.vi, word.meaning.en].some((text) =>
        normalizeVocabularySearch(text).includes(query),
      ),
  );
}

function shuffled<T>(items: readonly T[], random: () => number) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export type WordQuestion = { word: LanguageWord; options: LanguageWord[] };

/** A gloss can list several equivalent translations, separated by semicolons. */
function meaningParts(word: LanguageWord) {
  return (['vi', 'en'] as const).flatMap((language) =>
    word.meaning[language]
      .split(/[;,]|\s\/\s/)
      .map((part) => `${language}:${part.normalize('NFKC').toLowerCase().trim()}`),
  );
}

export function meaningsOverlap(first: LanguageWord, second: LanguageWord) {
  const parts = new Set(meaningParts(first));
  return meaningParts(second).some((part) => parts.has(part));
}

export function vocabularyPractice(
  selection: LanguageWord[],
  catalog: LanguageWord[],
  first?: LanguageWord,
  random: () => number = Math.random,
): WordQuestion[] {
  const remaining = shuffled(
    selection.filter((word) => word.id !== first?.id),
    random,
  );
  const queue = (first ? [first, ...remaining] : remaining).slice(0, 10);
  return queue.map((word) => {
    const candidates = shuffled(
      catalog.filter((other) => other.language === word.language && other.id !== word.id),
      random,
    );
    const options = [word];
    for (const candidate of candidates) {
      // Exclude matching translations even when one gloss lists additional senses.
      if (options.some((other) => meaningsOverlap(other, candidate))) continue;
      options.push(candidate);
      if (options.length === 4) break;
    }
    return { word, options: shuffled(options, random) };
  });
}

export async function saveWordPractice(word: LanguageWord, correct: boolean, started: number) {
  await logAttempt('vocabulary', correct ? 100 : 0, started, word.text, word.language);
}
