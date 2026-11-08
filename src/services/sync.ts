import { z } from 'zod';
import { create } from 'zustand';
import { wordSchema } from '../data/schema';
import { authFetch } from './auth';
import {
  attemptSchema,
  db,
  draftSchema,
  exportData,
  reviewSchema,
  settingsSchema,
  submissionSchema,
  vocabularyStudySchema,
} from './storage';

/** Every synced store and the field that orders its versions (newest wins). Attempts sync separately. */
const stores = {
  settings: { schema: settingsSchema, version: 'updated' },
  words: { schema: wordSchema, version: 'updated' },
  reviews: { schema: reviewSchema, version: 'lastReviewed' },
  drafts: { schema: draftSchema, version: 'updated' },
  submissions: { schema: submissionSchema, version: 'timestamp' },
  vocabularyStudy: { schema: vocabularyStudySchema, version: 'updated' },
} as const;
type Store = keyof typeof stores;
const storeNames = Object.keys(stores) as Store[];

/** Records saved before versions existed (settings, words) count as 0, so any edit wins. */
const versionOf = (store: Store, record: object) =>
  Number((record as Record<string, unknown>)[stores[store].version] ?? 0);

const responseSchema = z.object({
  attempts: z.array(attemptSchema),
  records: z.array(
    z.object({
      store: z.enum(storeNames as [Store, ...Store[]]),
      id: z.string(),
      data: z.unknown(),
    }),
  ),
});

export const useSync = create<{ status: 'idle' | 'syncing' | 'error'; lastSynced: number | null }>(
  () => ({ status: 'idle', lastSynced: null }),
);

/**
 * Merges this device with the signed-in account in both directions.
 * shortcut: deletions are not synced (a deleted custom word returns from the account); add tombstones if learners delete often.
 */
export async function syncNow() {
  if (useSync.getState().status === 'syncing') return false;
  useSync.setState({ status: 'syncing' });
  try {
    const local = await exportData();
    const records = storeNames.flatMap((store) =>
      (store === 'settings' ? [local.settings] : local[store]).map((data) => ({
        store,
        id: data.id,
        version: versionOf(store, data),
        data,
      })),
    );
    const response = await authFetch('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ attempts: local.attempts, records }),
    });
    if (!response.ok) throw new Error(`sync ${response.status}`);
    const remote = responseSchema.parse(await response.json());
    // Validate everything before the transaction so bad server data changes nothing.
    const incoming = storeNames.map((store) => ({
      store,
      rows: remote.records
        .filter((record) => record.store === store)
        .map((record) => stores[store].schema.parse(record.data)),
    }));
    await db.transaction('rw', db.tables, async () => {
      const known = new Set(await db.attempts.toCollection().primaryKeys());
      await db.attempts.bulkAdd(remote.attempts.filter((attempt) => !known.has(attempt.id)));
      for (const { store, rows } of incoming) {
        const table = db.table<object, string>(store);
        const current = await table.bulkGet(rows.map((row) => row.id));
        await table.bulkPut(
          rows.filter((row, i) => {
            const mine = current[i];
            return !mine || versionOf(store, mine) < versionOf(store, row);
          }),
        );
      }
    });
    useSync.setState({ status: 'idle', lastSynced: Date.now() });
    return true;
  } catch {
    useSync.setState({ status: 'error' });
    return false;
  }
}
