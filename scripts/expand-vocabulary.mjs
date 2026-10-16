import { readFileSync, writeFileSync } from 'node:fs';
import { log } from 'node:console';
import { URL } from 'node:url';

// Original EnglishUp content. Do not renumber existing cards: reviews reference their IDs.
const path = new URL('../src/data/vocabulary.json', import.meta.url);
const original = JSON.parse(readFileSync(path, 'utf8')).filter(
  (word) => !word.id.startsWith('v-common-') && !word.id.startsWith('v-extended-'),
);
const words = [...original];
const seen = new Set(words.map((word) => word.word.toLowerCase()));
for (const [file, prefix] of [
  ['common-vocabulary.txt', 'v-common-'],
  ['extended-english-vocabulary.txt', 'v-extended-'],
]) {
  const source = new URL(`./content/${file}`, import.meta.url);
  let topic, pos, level;
  for (const [index, raw] of readFileSync(source, 'utf8').split(/\r?\n/).entries()) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    if (line.startsWith('@')) {
      const fields = line.slice(1).split('|');
      if (fields.length !== 3 || fields.some((field) => !field.trim()))
        throw new Error(`Invalid header at ${file}:${index + 1}`);
      [topic, pos, level] = fields;
      continue;
    }
    const fields = line.split('|');
    const [word, meaning, definition, example] = fields;
    if (
      !topic ||
      ![
        'noun',
        'verb',
        'adjective',
        'adverb',
        'pronoun',
        'preposition',
        'conjunction',
        'number',
      ].includes(pos) ||
      !['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].includes(level) ||
      fields.length !== 4 ||
      fields.some((field) => !field.trim()) ||
      !example.toLowerCase().includes(word.toLowerCase())
    )
      throw new Error(`Invalid authored entry at ${file}:${index + 1}`);
    if (seen.has(word.toLowerCase()))
      throw new Error(`Duplicate word at ${file}:${index + 1}: ${word}`);
    seen.add(word.toLowerCase());
    words.push({
      id: `${prefix}${word
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
}
if (new Set(words.map((word) => word.id)).size !== words.length)
  throw new Error('Duplicate generated IDs');
let exampleIndex = 0;
const output = JSON.stringify(words, null, 2).replace(
  /^ {4}"examples": \[\n(?: {6}.*\n)+ {4}\],$/gm,
  () => `    "examples": ${JSON.stringify(words[exampleIndex++].examples)},`,
);
if (exampleIndex !== words.length) throw new Error('Could not serialize every example');
writeFileSync(path, output + '\n');
log(`${words.length} words (${words.length - original.length} generated from authored sources)`);
