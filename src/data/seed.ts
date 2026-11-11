import vocabulary from './vocabulary.json';
import itVocabulary from './vocabulary-it.json';
import phrasalVerbs from './vocabulary-phrasal.json';
import collocations from './vocabulary-collocations.json';
import commonVerbs from './vocabulary-verbs.json';
import structures from './structures.json';
import reading from './reading.json';
import listening from './listening.json';
import dictation from './dictation.json';
import speaking from './speaking.json';
import writing from './writing.json';
import translations from './translations.json';
import relationsBasic from './wordRelations-basic.json';
import relationsAdvanced from './wordRelations-advanced.json';
import grammarQuiz from './grammar-quiz.json';
import roadmaps from './roadmaps.json';
import tenses from './tenses.json';
import guides from './guides.json';
import type { ContentRow } from '../services/content';

/**
 * The seed lessons as the server returns them from GET /api/content. Tests only: the app never imports this
 * module, so the JSON stays out of the bundle; the server's `seed` command copies the same files into the database.
 */
const files: Record<string, { id: string }[]> = {
  word: [...vocabulary, ...itVocabulary, ...phrasalVerbs, ...collocations, ...commonVerbs],
  structure: structures,
  reading,
  listening,
  dictation,
  speaking,
  writing,
  translation: translations,
  relation: [...relationsBasic, ...relationsAdvanced],
  quiz: grammarQuiz,
  roadmap: roadmaps,
  tense: tenses,
  guide: guides,
};

export const seedRows: ContentRow[] = Object.entries(files).flatMap(([kind, items]) =>
  items.map((data) => ({
    kind,
    id: data.id,
    data,
    hidden: false,
    updatedAt: '2026-11-10T00:00:00Z',
  })),
);
