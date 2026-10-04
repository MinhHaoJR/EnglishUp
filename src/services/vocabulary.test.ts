import { vocabulary } from '../data/content';
import { groupWords, searchWords, paginateWords, WORDS_PER_PAGE } from './vocabulary';

test('grouping keeps custom topics and every word without mutating the input', () => {
  const words = [
    ...vocabulary,
    { ...vocabulary[0], id: 'custom', topic: 'My project', custom: true },
  ];
  const groups = groupWords(words);
  expect(groups.flatMap((group) => group.words)).toHaveLength(words.length);
  expect(groups.find((group) => group.topic === 'My project')?.words[0].id).toBe('custom');
  expect(words[0]).toBe(vocabulary[0]);
  expect(groupWords([])).toEqual([]);
});

test('pagination covers the complete catalog exactly once and clamps after results shrink', () => {
  const first = paginateWords(vocabulary, 0);
  expect(first.words).toHaveLength(WORDS_PER_PAGE);
  const pages = Array.from(
    { length: first.pageCount },
    (_, page) => paginateWords(vocabulary, page).words,
  );
  expect(pages.flat().map((word) => word.id)).toEqual(vocabulary.map((word) => word.id));
  const narrowed = vocabulary.filter((word) => word.topic === 'People and family');
  const last = paginateWords(narrowed, 99);
  expect(last.page).toBe(1);
  expect(last.words).toHaveLength(20);
  expect(paginateWords([], 99)).toEqual({ page: 0, pageCount: 1, words: [] });
});

test('search supports English, Vietnamese, missing accents and empty results', () => {
  expect(searchWords(vocabulary, '  PRIMARY KEY ')).toHaveLength(1);
  expect(searchWords(vocabulary, 'co so du lieu').map((word) => word.word)).toContain('database');
  expect(searchWords(vocabulary, 'ĐỊNH TUYẾN').map((word) => word.word)).toContain('router');
  expect(searchWords(vocabulary, 'no-such-word')).toEqual([]);
  expect(searchWords(vocabulary, '   ')).toHaveLength(vocabulary.length);
});
