import { wordSchema, type Word } from '../data/schema';
export const headers = [
  'word',
  'ipa',
  'pos',
  'meaning',
  'definition',
  'examples',
  'level',
  'topic',
] as const;
export function parseCSV(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = '';
  let quoted = false;
  let closed = false;
  const source = text.replace(/^\uFEFF/, '');
  for (let i = 0; i < source.length; i++) {
    const c = source[i];
    if (closed && c !== ',' && c !== '\n' && c !== '\r')
      throw new Error('Unexpected character after quote');
    if (c === '"') {
      if (quoted && source[i + 1] === '"') {
        field += '"';
        i++;
      } else if (quoted) {
        quoted = false;
        closed = true;
      } else if (field === '') {
        quoted = true;
      } else throw new Error('Unexpected quote');
    } else if (c === ',' && !quoted) {
      row.push(field);
      field = '';
      closed = false;
    } else if ((c === '\n' || c === '\r') && !quoted) {
      if (c === '\r' && source[i + 1] === '\n') i++;
      row.push(field);
      if (row.some(Boolean)) rows.push(row);
      row = [];
      field = '';
      closed = false;
    } else field += c;
  }
  if (quoted) throw new Error('Unclosed quote');
  row.push(field);
  if (row.some(Boolean)) rows.push(row);
  return rows;
}
export function importCSV(text: string): Word[] {
  const [head, ...rows] = parseCSV(text);
  if (!head || headers.some((h) => !head.includes(h)) || new Set(head).size !== head.length)
    throw new Error('Missing or duplicate CSV headers');
  return rows.map((r, i) => {
    if (r.length !== head.length) throw new Error(`Row ${i + 2}: column count`);
    const get = (key: string) => r[head.indexOf(key)].trim();
    return wordSchema.parse({
      id: crypto.randomUUID(),
      word: get('word'),
      ipa: get('ipa'),
      pos: get('pos'),
      meaning: get('meaning'),
      definition: get('definition'),
      examples: get('examples').split(' || ').filter(Boolean),
      level: get('level'),
      topic: get('topic'),
      custom: true,
    });
  });
}
export function exportCSV(words: Word[]) {
  const escape = (s: string) =>
    `"${(/^[=+@\-\t\r]/.test(s) ? "'" : '') + s.replaceAll('"', '""')}"`;
  return (
    '\uFEFF' +
    [
      headers.join(','),
      ...words.map((w) =>
        headers.map((h) => escape(h === 'examples' ? w.examples.join(' || ') : w[h])).join(','),
      ),
    ].join('\r\n')
  );
}
