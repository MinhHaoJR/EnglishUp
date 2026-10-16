import { z } from 'zod';
import rawTranslations from './translations.json';
import { levelSchema } from './schema';
export const translations = z
  .array(
    z.object({
      id: z.string().min(1),
      level: levelSchema,
      topic: z.string().min(1),
      en: z.array(z.string().trim().min(1)).min(1),
      vi: z.array(z.string().trim().min(1)).min(1),
    }),
  )
  .min(16)
  .parse(rawTranslations);
if (new Set(translations.map((item) => item.id)).size !== translations.length)
  throw new Error('Duplicate translation IDs');
import {
  readingSchema,
  listeningSchema,
  dictationSchema,
  speakingSchema,
  writingSchema,
} from './schema';
import rawWriting from './writing.json';
export const writingPrompts = z.array(writingSchema).min(10).parse(rawWriting);
import rawSpeaking from './speaking.json';
export const speakingPrompts = z.array(speakingSchema).min(16).parse(rawSpeaking);
import rawListening from './listening.json';
import rawDictation from './dictation.json';
export const listenings = z.array(listeningSchema).min(6).parse(rawListening);
export const dictations = z.array(dictationSchema).min(10).parse(rawDictation);
import rawReading from './reading.json';
export const readings = z.array(readingSchema).min(6).parse(rawReading);
export { vocabulary } from './vocabularyContent';
