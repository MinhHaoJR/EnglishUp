import type { WordRelation } from '../data/wordRelations';
import type { Level } from '../data/schema';
import { logAttempt } from './storage';

export type RelationKind = 'synonym' | 'antonym';
export type RelationMode = RelationKind | 'mixed';
export type RelationQuestion = {
  id: string;
  entry: WordRelation;
  kind: RelationKind;
  options: string[];
  answer: string;
};

function normalizeSearch(value: string) {
  return value
    .normalize('NFKC')
    .normalize('NFD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/đ/g, 'd')
    .replace(/\s+/g, ' ')
    .trim();
}

export function filterRelations(entries: WordRelation[], level: Level | 'all', search: string) {
  const query = normalizeSearch(search);
  return entries.filter(
    (entry) =>
      (level === 'all' || entry.level === level) &&
      [
        entry.word,
        entry.meaning,
        entry.definition,
        ...entry.synonyms.flatMap((word) => [word.word, word.meaning]),
        ...entry.antonyms.flatMap((word) => [word.word, word.meaning]),
      ].some((value) => normalizeSearch(value).includes(query)),
  );
}

function shuffle<T>(items: T[], random: () => number) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/** Each question contrasts two editorially checked senses, avoiding ambiguous random distractors. */
export function createRelationSession(
  entries: WordRelation[],
  mode: RelationMode,
  limit = 10,
  random: () => number = Math.random,
): RelationQuestion[] {
  const size = Number.isFinite(limit) ? Math.max(0, Math.min(10, Math.floor(limit))) : 10;
  const firstKind: RelationKind = random() < 0.5 ? 'synonym' : 'antonym';
  return shuffle(entries, random)
    .slice(0, size)
    .map((entry, index) => {
      const kind =
        mode === 'mixed'
          ? index % 2 === 0
            ? firstKind
            : firstKind === 'synonym'
              ? 'antonym'
              : 'synonym'
          : mode;
      const answer = (kind === 'synonym' ? entry.synonyms : entry.antonyms)[0].word;
      return {
        id: `${entry.id}-${kind}`,
        entry,
        kind,
        answer,
        options: shuffle([entry.synonyms[0].word, entry.antonyms[0].word], random),
      };
    });
}

export async function saveRelationAnswer(
  question: RelationQuestion,
  answer: string,
  started: number,
) {
  if (!question.options.includes(answer) || !Number.isFinite(started)) {
    throw new Error('Choose a valid relation answer before saving');
  }
  await logAttempt(
    'vocabulary',
    answer === question.answer ? 100 : 0,
    started,
    `${question.kind === 'synonym' ? 'Synonym' : 'Antonym'} · ${question.entry.level}: ${question.entry.word}`,
    'en',
  );
}
