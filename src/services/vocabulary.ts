import type { Word } from '../data/schema';

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
