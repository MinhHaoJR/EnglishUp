import { readFileSync, writeFileSync } from 'node:fs';
import { log } from 'node:console';
import { URL } from 'node:url';
import { z } from 'zod';

const topics = new Set([
  'greetings',
  'people',
  'home',
  'food',
  'drinks',
  'shopping',
  'travel',
  'transport',
  'time',
  'nature',
  'animals',
  'body',
  'health',
  'school',
  'work',
  'technology',
  'activities',
  'verbs',
  'adjectives',
  'society',
]);
const rowSchema = z.array(z.string().trim().min(1)).length(7);
const words = [];
for (const [language, file] of [
  ['ja', 'japanese'],
  ['zh', 'chinese'],
]) {
  const source = readFileSync(new URL(`./content/${file}-vocabulary.txt`, import.meta.url), 'utf8');
  const entries = source
    .split(/\r?\n/)
    .filter((line) => line.trim() && !line.startsWith('#'))
    .map((line, index) => {
      const [id, topic, text, reading, romanization, vi, en] = rowSchema.parse(line.split('|'));
      if (!new RegExp(`^${language}-vocab-\\d{4}$`).test(id) || !topics.has(topic))
        throw new Error(`Invalid ID or topic: ${file} row ${index + 1}`);
      return { id, language, text, reading, romanization, meaning: { vi, en }, topic };
    });
  if (entries.length < 2000)
    throw new Error(`${file}: expected at least 2000 entries, received ${entries.length}`);
  if (
    new Set(entries.map((word) => word.id)).size !== entries.length ||
    new Set(entries.map((word) => word.text.normalize('NFKC'))).size !== entries.length
  )
    throw new Error(`Duplicate IDs or headwords in ${file}`);
  words.push(...entries);
  log(`${file}: ${entries.length} entries`);
}
// Both catalogs are validated before replacing the generated file.
writeFileSync(
  new URL('../src/data/language-vocabulary.json', import.meta.url),
  JSON.stringify(words, null, 2) + '\n',
);
