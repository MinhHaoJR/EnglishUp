import { z } from 'zod';
import rawItWords from './vocabulary-it.json';
import { wordSchema } from './schema';

export const itVocabulary = z.array(wordSchema).min(1).parse(rawItWords);
