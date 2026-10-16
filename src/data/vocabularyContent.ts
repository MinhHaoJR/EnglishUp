import { z } from 'zod';
import rawWords from './vocabulary.json';
import { wordSchema } from './schema';
import { itVocabulary } from './itVocabularyContent';

const coreVocabulary = z.array(wordSchema).min(1500).parse(rawWords);
export const vocabulary = [...coreVocabulary, ...itVocabulary];
if (new Set(vocabulary.map((word) => word.id)).size !== vocabulary.length)
  throw new Error('Duplicate content IDs');
