import { z } from 'zod';
import { create } from 'zustand';

/** Tokens live in localStorage, outside Dexie, so they never enter JSON backups. */
const STORAGE_KEY = 'englishup.session';
const sessionSchema = z.object({
  email: z.string().email(),
  accessToken: z.string().min(1),
  refreshToken: z.string().min(1),
  expiresAt: z.number(),
});
type Session = z.infer<typeof sessionSchema>;
const tokensSchema = z.object({
  accessToken: z.string().min(1),
  refreshToken: z.string().min(1),
  expiresIn: z.number().positive(),
});

export type AuthErrorKind = 'invalid' | 'locked' | 'exists' | 'password' | 'email' | 'network';
export class AuthError extends Error {
  constructor(readonly kind: AuthErrorKind) {
    super(kind);
  }
}

export const useAuth = create<{ email: string | null }>(() => ({ email: null }));

function readSession(): Session | null {
  try {
    const parsed = sessionSchema.safeParse(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null'));
    return parsed.success ? parsed.data : null;
  } catch {
    return null;
  }
}
function writeSession(session: Session | null) {
  try {
    if (session) localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    else localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* Storage blocked: the session still works until reload. */
  }
  useAuth.setState({ email: session?.email ?? null });
}

async function post(path: string, body: unknown) {
  try {
    return await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch {
    throw new AuthError('network');
  }
}
async function storeTokens(email: string, response: Response) {
  const tokens = tokensSchema.parse(await response.json());
  writeSession({
    email,
    accessToken: tokens.accessToken,
    refreshToken: tokens.refreshToken,
    expiresAt: Date.now() + tokens.expiresIn * 1000,
  });
}

export async function login(email: string, password: string) {
  const response = await post('/api/login', { email: email.trim(), password });
  if (response.status === 401) {
    const problem = (await response.json().catch(() => ({}))) as { detail?: string };
    throw new AuthError(problem.detail === 'LockedOut' ? 'locked' : 'invalid');
  }
  if (!response.ok) throw new AuthError('network');
  await storeTokens(email.trim(), response);
}

export async function register(email: string, password: string) {
  const response = await post('/api/register', { email: email.trim(), password });
  if (response.status === 400) {
    const { errors = {} } = (await response.json().catch(() => ({}))) as {
      errors?: Record<string, string[]>;
    };
    const codes = Object.keys(errors);
    throw new AuthError(
      codes.some((code) => code.startsWith('Duplicate'))
        ? 'exists'
        : codes.some((code) => code.startsWith('Password'))
          ? 'password'
          : 'email',
    );
  }
  if (!response.ok) throw new AuthError('network');
  await login(email, password);
}

export function logout() {
  // shortcut: bearer tokens expire on their own (1 h, refresh 14 days); add server revocation if accounts are shared devices.
  writeSession(null);
}

async function refresh(session: Session) {
  const response = await post('/api/refresh', { refreshToken: session.refreshToken });
  if (!response.ok) {
    logout();
    return null;
  }
  await storeTokens(session.email, response);
  return readSession();
}

/** Calls the API as the signed-in learner, refreshing an expiring token first. */
export async function authFetch(path: string, init: RequestInit = {}) {
  let session = readSession();
  if (!session) throw new AuthError('invalid');
  if (session.expiresAt - 30_000 < Date.now()) session = await refresh(session);
  if (!session) throw new AuthError('invalid');
  const headers = new Headers(init.headers);
  headers.set('Authorization', `Bearer ${session.accessToken}`);
  let response: Response;
  try {
    response = await fetch(path, { ...init, headers });
  } catch {
    throw new AuthError('network');
  }
  if (response.status === 401) {
    logout();
    throw new AuthError('invalid');
  }
  return response;
}

export class ApiError extends Error {
  constructor(readonly status: number) {
    super(`HTTP ${status}`);
  }
}

/** Calls the API and validates the JSON reply; rejects with ApiError on HTTP errors. */
export async function fetchJson<T>(schema: z.ZodType<T>, path: string, init?: RequestInit) {
  const response = await authFetch(path, init);
  if (!response.ok) throw new ApiError(response.status);
  return schema.parse(await response.json());
}

/** Restores the saved session; an offline server keeps it, a rejected token clears it. */
export async function restoreSession() {
  const session = readSession();
  useAuth.setState({ email: session?.email ?? null });
  if (!session) return;
  try {
    await authFetch('/api/manage/info');
  } catch {
    /* authFetch already signed out when the server rejected the session. */
  }
}
