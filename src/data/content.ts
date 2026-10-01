import { z } from 'zod';
import rawWords from './vocabulary.json';
import { wordSchema,readingSchema } from './schema';
import rawReading from './reading.json';
export const readings=z.array(readingSchema).min(6).parse(rawReading);
export const vocabulary=z.array(wordSchema).min(150).parse(rawWords);
if(new Set(vocabulary.map(x=>x.id)).size!==vocabulary.length)throw new Error('Duplicate content IDs');
