import { z } from 'zod';
import rawWords from './vocabulary.json';
import { wordSchema } from './schema';
export const vocabulary=z.array(wordSchema).min(150).parse(rawWords);
if(new Set(vocabulary.map(x=>x.id)).size!==vocabulary.length)throw new Error('Duplicate content IDs');
