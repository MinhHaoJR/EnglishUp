import { z } from 'zod';
import {
  dictations,
  listenings,
  readings,
  speakingPrompts,
  structures,
  vocabulary,
  writingPrompts,
} from '../data/content';
import {
  dictationSchema,
  listeningSchema,
  readingSchema,
  speakingSchema,
  structureSchema,
  wordSchema,
  writingSchema,
} from '../data/schema';
import { ApiError, authFetch } from './auth';

/**
 * Each kind of learning item an admin can add, edit or hide, with the app's schema and the live list
 * the pages read. The lists are rebuilt in place, so every page keeps importing them as before.
 */
export const contentKinds = {
  word: { schema: wordSchema, items: vocabulary },
  structure: { schema: structureSchema, items: structures },
  reading: { schema: readingSchema, items: readings },
  listening: { schema: listeningSchema, items: listenings },
  dictation: { schema: dictationSchema, items: dictations },
  speaking: { schema: speakingSchema, items: speakingPrompts },
  writing: { schema: writingSchema, items: writingPrompts },
} as const;
export type ContentKind = keyof typeof contentKinds;
type Item = { id: string };

/** The lessons as shipped in src/data, captured before any admin change. */
export const bundled = Object.fromEntries(
  Object.entries(contentKinds).map(([kind, { items }]) => [kind, [...(items as Item[])]]),
) as Record<ContentKind, Item[]>;

const rowSchema = z.object({
  kind: z.string(),
  id: z.string(),
  data: z.unknown().optional(),
  hidden: z.boolean(),
  updatedAt: z.string(),
});
export type ContentRow = z.infer<typeof rowSchema>;

export async function fetchContentRows() {
  const response = await fetch('/api/content', { signal: AbortSignal.timeout(5000) });
  if (!response.ok) throw new ApiError(response.status);
  return z.array(rowSchema).parse(await response.json());
}

/** Validates an admin row against the app's schema; null when it would break a page. */
export function parseRow(row: ContentRow): Item | null {
  const kind = contentKinds[row.kind as ContentKind];
  const parsed = kind?.schema.safeParse(row.data);
  return parsed?.success && parsed.data.id === row.id ? parsed.data : null;
}

/** Rebuilds every list: the bundled items, then the admin's rows on top. Invalid rows are skipped. */
export function applyContent(rows: ContentRow[]) {
  for (const kind of Object.keys(contentKinds) as ContentKind[]) {
    const next = [...bundled[kind]];
    for (const row of rows.filter((r) => r.kind === kind)) {
      const at = next.findIndex((item) => item.id === row.id);
      if (row.hidden) {
        if (at >= 0) next.splice(at, 1);
        continue;
      }
      const item = parseRow(row);
      if (!item) continue;
      if (at >= 0) next[at] = item;
      else next.push(item);
    }
    const list = contentKinds[kind].items as Item[];
    list.splice(0, list.length, ...next);
  }
}

let loading: Promise<void> | null = null;
/**
 * Loads the admin's changes once per app start (or again with force). Offline or with the server
 * down it keeps the bundled lessons; the service worker serves the last answer when offline.
 */
export function loadContent(force = false) {
  if (!loading || force)
    loading = fetchContentRows()
      .then(applyContent)
      .catch(() => undefined);
  return loading;
}

async function send(path: string, init: RequestInit) {
  const response = await authFetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) throw new ApiError(response.status);
}
const address = (kind: ContentKind, id: string) =>
  `/api/admin/content/${kind}/${encodeURIComponent(id)}`;

export const saveContent = (kind: ContentKind, item: Item) =>
  send(address(kind, item.id), { method: 'PUT', body: JSON.stringify({ data: item }) });

export const hideContent = (kind: ContentKind, id: string, hidden: boolean) =>
  send(`${address(kind, id)}/hide`, { method: 'POST', body: JSON.stringify({ hidden }) });

/** Removes the admin's row: an added item disappears, an edited bundled item returns to the original. */
export const resetContent = (kind: ContentKind, id: string) =>
  send(address(kind, id), { method: 'DELETE' });
