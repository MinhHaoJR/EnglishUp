import { readFileSync, writeFileSync } from 'node:fs';
import { log } from 'node:console';
import { URL } from 'node:url';

// Original EnglishUp content. Do not renumber existing cards: reviews reference their IDs.
const path = new URL('../src/data/vocabulary.json', import.meta.url);
const source = new URL('./content/common-vocabulary.txt', import.meta.url);
const original = JSON.parse(readFileSync(path, 'utf8')).filter(
  (word) => !word.id.startsWith('v-common-'),
);
const words = [...original];
const seen = new Set(words.map((word) => word.word.toLowerCase()));
let topic, pos, level;
for (const [index, raw] of readFileSync(source, 'utf8').split(/\r?\n/).entries()) {
  const line = raw.trim();
  if (!line || line.startsWith('#')) continue;
  if (line.startsWith('@')) {
    [topic, pos, level] = line.slice(1).split('|');
    continue;
  }
  const fields = line.split('|');
  const [word, meaning, definition, example] = fields;
  if (
    !topic ||
    !pos ||
    !['A1', 'A2', 'B1', 'B2'].includes(level) ||
    fields.length !== 4 ||
    fields.some((field) => !field.trim())
  )
    throw new Error(`Invalid authored entry at line ${index + 1}`);
  if (seen.has(word.toLowerCase())) throw new Error(`Duplicate word at line ${index + 1}: ${word}`);
  seen.add(word.toLowerCase());
  words.push({
    id: `v-common-${word
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/-$/, '')}`,
    word,
    ipa: '',
    pos,
    meaning,
    definition,
    examples: [example],
    level,
    topic,
  });
}
if (new Set(words.map((word) => word.id)).size !== words.length)
  throw new Error('Duplicate generated IDs');
writeFileSync(path, JSON.stringify(words, null, 2) + '\n');
log(`${words.length} words (${words.length - original.length} additions)`);
