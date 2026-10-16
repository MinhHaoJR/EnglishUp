import { readFileSync, writeFileSync } from 'node:fs';
import { log } from 'node:console';
import { URL } from 'node:url';

// Original EnglishUp content. Do not renumber existing cards: reviews reference their IDs.
const corePath = new URL('../src/data/vocabulary.json', import.meta.url);
const itPath = new URL('../src/data/vocabulary-it.json', import.meta.url);
const original = JSON.parse(readFileSync(corePath, 'utf8')).filter(
  (word) =>
    !word.id.startsWith('v-common-') &&
    !word.id.startsWith('v-extended-') &&
    !word.id.startsWith('v-it-'),
);
const words = [...original];
const itWords = [];
const seen = new Set(words.map((word) => word.word.toLowerCase()));
for (const [file, prefix, output] of [
  ['common-vocabulary.txt', 'v-common-', words],
  ['extended-english-vocabulary.txt', 'v-extended-', words],
  ['it-vocabulary.txt', 'v-it-', itWords],
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
    output.push({
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
const all = [...words, ...itWords];
if (new Set(all.map((word) => word.id)).size !== all.length)
  throw new Error('Duplicate generated IDs');
function serialize(entries) {
  let exampleIndex = 0;
  const output = JSON.stringify(entries, null, 2).replace(
    /^ {4}"examples": \[\n(?: {6}.*\n)+ {4}\],$/gm,
    () => `    "examples": ${JSON.stringify(entries[exampleIndex++].examples)},`,
  );
  if (exampleIndex !== entries.length) throw new Error('Could not serialize every example');
  return output + '\n';
}
const coreOutput = serialize(words);
const itOutput = serialize(itWords);
writeFileSync(corePath, coreOutput);
writeFileSync(itPath, itOutput);
log(`${all.length} words (${all.length - original.length} generated from authored sources)`);
