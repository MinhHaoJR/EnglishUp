import { z } from 'zod';
import { create } from 'zustand';
import { ApiError, authFetch, fetchJson, useAuth } from './auth';

/**
 * Whether the signed-in account is in the server's Admin role (checked on the server, not trusted).
 * `checkedFor` is the email the answer belongs to, so a page never acts on the previous account's answer.
 */
export const useAdmin = create<{ isAdmin: boolean; checkedFor: string | null }>(() => ({
  isAdmin: false,
  checkedFor: null,
}));

const meSchema = z.object({ email: z.string(), isAdmin: z.boolean() });

export async function refreshAdmin() {
  const email = useAuth.getState().email;
  if (!email) return useAdmin.setState({ isAdmin: false, checkedFor: null });
  let isAdmin = false;
  try {
    isAdmin = (await fetchJson(meSchema, '/api/me')).isAdmin;
  } catch {
    /* Offline or rejected: treat as a learner; the server still guards /api/admin. */
  }
  // Another account signed in meanwhile: its own check will answer.
  if (useAuth.getState().email === email) useAdmin.setState({ isAdmin, checkedFor: email });
}

/**
 * Tells the server the app is open: once now, every minute while the tab is visible, and when it
 * becomes visible again. The admin page counts anyone seen in the last two minutes as online.
 */
export function startPresence(intervalMs = 60_000) {
  const beat = () => {
    if (!useAuth.getState().email || document.visibilityState !== 'visible') return;
    void authFetch('/api/presence', { method: 'POST' }).catch(() => undefined);
  };
  const onVisible = () => {
    if (document.visibilityState === 'visible') beat();
  };
  const stopAuth = useAuth.subscribe((state, previous) => {
    if (state.email === previous.email) return;
    beat();
    void refreshAdmin();
  });
  beat();
  void refreshAdmin();
  const timer = setInterval(beat, intervalMs);
  document.addEventListener('visibilitychange', onVisible);
  return () => {
    clearInterval(timer);
    document.removeEventListener('visibilitychange', onVisible);
    stopAuth();
  };
}

const overviewSchema = z.object({
  users: z.number().int(),
  online: z.number().int(),
  offline: z.number().int(),
  activeToday: z.number().int(),
  locked: z.number().int(),
  admins: z.number().int(),
  attemptsToday: z.number().int(),
  questionsToday: z.number().int(),
  gamesToday: z.number().int(),
  knowledgeChunks: z.number().int(),
  onlineWindowSeconds: z.number().int(),
  at: z.string(),
});
export type Overview = z.infer<typeof overviewSchema>;

const usersSchema = z.array(
  z.object({
    id: z.string(),
    email: z.string(),
    displayName: z.string().nullish(),
    showOnLeaderboard: z.boolean(),
    isAdmin: z.boolean(),
    locked: z.boolean(),
    lastSeenAt: z.string().nullish(),
    online: z.boolean(),
    points: z.number().int(),
    attempts: z.number().int(),
  }),
);
export type AdminUser = z.infer<typeof usersSchema>[number];

export const fetchOverview = () => fetchJson(overviewSchema, '/api/admin/overview');

export const fetchUsers = (search = '') =>
  fetchJson(
    usersSchema,
    `/api/admin/users${search.trim() ? `?search=${encodeURIComponent(search.trim())}` : ''}`,
  );

async function post(path: string, body?: unknown) {
  const response = await authFetch(path, {
    method: 'POST',
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) throw new ApiError(response.status);
}

export const setLocked = (id: string, locked: boolean) =>
  post(`/api/admin/users/${encodeURIComponent(id)}/lock`, { locked });

export const hideFromLeaderboard = (id: string) =>
  post(`/api/admin/users/${encodeURIComponent(id)}/hide`);
