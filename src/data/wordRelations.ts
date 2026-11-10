import { z } from 'zod';
import { levelSchema } from './schema';

const text = z.string().trim().min(1);
const relatedWordSchema = z.object({ word: text, meaning: text, example: text });
const normalized = (value: string) => value.normalize('NFKC').toLowerCase().trim();

export const wordRelationSchema = z
  .object({
    id: z.string().regex(/^rel-(a1|a2|b1|b2|c1|c2)-[a-z-]+$/),
    level: levelSchema,
    word: text,
    pos: z.enum(['adjective', 'verb', 'noun', 'adverb']),
    meaning: text,
    definition: text,
    example: text,
    synonyms: z.array(relatedWordSchema).length(1),
    antonyms: z.array(relatedWordSchema).length(1),
    usageNote: z.object({ vi: text, en: text }),
  })
  .superRefine((entry, ctx) => {
    const terms = [
      entry.word,
      ...entry.synonyms.map((w) => w.word),
      ...entry.antonyms.map((w) => w.word),
    ].map(normalized);
    if (new Set(terms).size !== terms.length) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Headword, synonym and antonym must differ',
      });
    }
    if (!entry.id.startsWith(`rel-${entry.level.toLowerCase()}-`)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Relation ID level does not match the lesson',
      });
    }
  });

export type WordRelation = z.infer<typeof wordRelationSchema>;
/** Filled from the server's content library by services/content.ts, like the lists in ./content. */
export const wordRelations: WordRelation[] = [];
