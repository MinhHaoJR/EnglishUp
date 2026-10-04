import type { Word } from '../data/schema';

export const WORDS_PER_PAGE = 30;

export function paginateWords(words: Word[], requestedPage: number) {
  const pageCount = Math.max(1, Math.ceil(words.length / WORDS_PER_PAGE));
  const page = Math.max(0, Math.min(requestedPage, pageCount - 1));
  return {
    page,
    pageCount,
    words: words.slice(page * WORDS_PER_PAGE, (page + 1) * WORDS_PER_PAGE),
  };
}

export function groupWords(words: Word[]) {
  const groups = new Map<string, Word[]>();
  for (const word of words) {
    const group = groups.get(word.topic) ?? [];
    group.push(word);
    groups.set(word.topic, group);
  }
  return Array.from(groups, ([topic, entries]) => ({ topic, words: entries }));
}

export function searchWords(words: Word[], search: string) {
  const normalize = (value: string) =>
    value.normalize('NFD').replace(/\p{M}/gu, '').replace(/[đĐ]/g, 'd').toLowerCase().trim();
  const query = normalize(search);
  return words.filter((word) => normalize(`${word.word} ${word.meaning}`).includes(query));
}
