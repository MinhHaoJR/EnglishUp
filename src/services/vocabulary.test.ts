import { vocabulary } from '../data/content';
import { groupWords, searchWords } from './vocabulary';

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

test('search supports English, Vietnamese, missing accents and empty results', () => {
  expect(searchWords(vocabulary, '  PRIMARY KEY ')).toHaveLength(1);
  expect(searchWords(vocabulary, 'co so du lieu').map((word) => word.word)).toContain('database');
  expect(searchWords(vocabulary, 'ĐỊNH TUYẾN').map((word) => word.word)).toContain('router');
  expect(searchWords(vocabulary, 'no-such-word')).toEqual([]);
  expect(searchWords(vocabulary, '   ')).toHaveLength(vocabulary.length);
});
