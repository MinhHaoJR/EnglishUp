import { z } from 'zod';
import { create } from 'zustand';
import {
  dictations,
  listenings,
  readings,
  speakingPrompts,
  structures,
  translations,
  vocabulary,
  writingPrompts,
} from '../data/content';
import {
  dictationSchema,
  listeningSchema,
  readingSchema,
  speakingSchema,
  structureSchema,
  translationSchema,
  wordSchema,
  writingSchema,
} from '../data/schema';
import { wordRelationSchema, wordRelations } from '../data/wordRelations';
import { ApiError, authFetch } from './auth';
import { db } from './storage';

/**
 * Each kind of learning item in the server's library, with the app's schema and the live list the pages read.
 * The lists are rebuilt in place, so every page keeps importing them from data/content.
 */
export const contentKinds = {
  word: { schema: wordSchema, items: vocabulary },
  structure: { schema: structureSchema, items: structures },
  reading: { schema: readingSchema, items: readings },
  listening: { schema: listeningSchema, items: listenings },
  dictation: { schema: dictationSchema, items: dictations },
  speaking: { schema: speakingSchema, items: speakingPrompts },
  writing: { schema: writingSchema, items: writingPrompts },
  translation: { schema: translationSchema, items: translations },
  relation: { schema: wordRelationSchema, items: wordRelations },
} as const;
export type ContentKind = keyof typeof contentKinds;
type Item = { id: string };

const rowSchema = z.object({
  kind: z.string(),
  id: z.string(),
  data: z.unknown(),
  hidden: z.boolean(),
  updatedAt: z.string(),
});
export type ContentRow = z.infer<typeof rowSchema>;
const rowsSchema = z.array(rowSchema);

/** The whole library; the server's ETag lets the browser answer a repeat visit with a 304 instead of 1 MB. */
export async function fetchContentRows() {
  const response = await fetch('/api/content', { signal: AbortSignal.timeout(10_000) });
  if (!response.ok) throw new ApiError(response.status);
  return rowsSchema.parse(await response.json());
}

/** Validates a row against the app's schema; null when it would break a page. */
export function parseRow(row: ContentRow): Item | null {
  const kind = contentKinds[row.kind as ContentKind];
  const parsed = kind?.schema.safeParse(row.data);
  return parsed?.success && parsed.data.id === row.id ? parsed.data : null;
}

/** Rebuilds every list from the rows, in the server's order. Hidden and invalid rows are skipped. */
export function applyContent(rows: ContentRow[]) {
  for (const kind of Object.keys(contentKinds) as ContentKind[]) {
    const next = rows
      .filter((row) => row.kind === kind && !row.hidden)
      .map(parseRow)
      .filter((item): item is Item => item !== null);
    const list = contentKinds[kind].items as Item[];
    list.splice(0, list.length, ...next);
  }
}

/** live: from the server; offline: the copy saved on this device; missing: neither, so there are no lessons. */
export type ContentStatus = 'loading' | 'live' | 'offline' | 'missing';
export const useContent = create<{ status: ContentStatus }>(() => ({ status: 'loading' }));

let loading: Promise<void> | null = null;
/**
 * Loads the library once per app start (or again with force). Each download is saved in Dexie, so learners
 * keep practising offline; only the very first visit needs the network.
 */
export function loadContent(force = false) {
  if (!loading || force)
    loading = (async () => {
      try {
        const rows = await fetchContentRows();
        applyContent(rows);
        useContent.setState({ status: 'live' });
        await db.lessons.put({ id: 'library', rows, saved: Date.now() }).catch(() => undefined);
      } catch {
        const saved = rowsSchema.safeParse(
          (await db.lessons.get('library').catch(() => undefined))?.rows,
        );
        if (saved.success) {
          applyContent(saved.data);
          useContent.setState({ status: 'offline' });
        } else useContent.setState({ status: 'missing' });
      }
    })();
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

/** Removes the item from the library for good; hiding is the reversible choice. */
export const deleteContent = (kind: ContentKind, id: string) =>
  send(address(kind, id), { method: 'DELETE' });
