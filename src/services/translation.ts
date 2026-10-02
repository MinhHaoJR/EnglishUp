import type { Word, Level } from '../data/schema';

export type TranslationDirection = 'vi-en' | 'en-vi';
export interface TranslationItem {
  id: string;
  level: Level;
  topic: string;
  en: string[];
  vi: string[];
}

// Keep Vietnamese accents: ma and má are different words.
export function normalizeTranslation(text: string) {
  return text
    .normalize('NFC')
    .toLocaleLowerCase()
    .replace(/[’‘]/g, "'")
    .replace(/[.,!?;:“”"…]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function matchesTranslation(answer: string, accepted: string[]) {
  const normalized = normalizeTranslation(answer);
  return !!normalized && accepted.some((text) => normalizeTranslation(text) === normalized);
}

export function wordTranslation(word: Word): TranslationItem {
  return {
    id: word.id,
    level: word.level,
    topic: word.topic,
    en: [word.word],
    vi: [
      ...new Set([
        word.meaning,
        ...word.meaning
          .split(/[,;]/)
          .map((s) => s.trim())
          .filter(Boolean),
      ]),
    ],
  };
}

export function translationSides(item: TranslationItem, direction: TranslationDirection) {
  return direction === 'vi-en'
    ? { prompt: item.vi[0], answers: item.en, language: 'en' }
    : { prompt: item.en[0], answers: item.vi, language: 'vi' };
}

export function translationSession(items: TranslationItem[]) {
  const shuffled = [...items];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, 10);
}
