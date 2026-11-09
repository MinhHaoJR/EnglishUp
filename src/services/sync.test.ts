import { useAuth } from './auth';
import { db, defaults, logAttempt, resetData, type Attempt, type Review } from './storage';
import { startAutoSync, syncNow, useSync } from './sync';

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
const attempt = (id: string): Attempt => ({
  id,
  skill: 'reading',
  score: 80,
  duration: 60,
  timestamp: 1000,
  label: 'Passage 1',
});
const review = (id: string, lastReviewed: number): Review => ({
  id,
  ease: 2.5,
  interval: 1,
  repetitions: 1,
  due: lastReviewed + 86_400_000,
  introduced: 1,
  lastReviewed,
  correct: 1,
  total: 1,
});

let fetchMock: ReturnType<typeof vi.fn>;
beforeEach(async () => {
  await resetData();
  useSync.setState({ status: 'idle', lastSynced: null, points: null });
  useAuth.setState({ email: null });
  localStorage.setItem(
    'englishup.session',
    JSON.stringify({
      email: 'learner@example.test',
      accessToken: 'access',
      refreshToken: 'refresh',
      expiresAt: Date.now() + 3_600_000,
    }),
  );
  fetchMock = vi.fn();
  vi.stubGlobal('fetch', fetchMock);
});
afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
});

it('pushes local records with versions and keeps the newest copy of each record', async () => {
  await db.attempts.add(attempt('local'));
  await db.reviews.bulkAdd([review('newer-here', 900), review('newer-there', 100)]);
  await db.settings.put({ ...defaults, theme: 'dark', updated: 50 });
  fetchMock.mockResolvedValueOnce(
    json({
      attempts: [attempt('local'), attempt('other-device')],
      records: [
        { store: 'reviews', id: 'newer-here', data: review('newer-here', 500) },
        { store: 'reviews', id: 'newer-there', data: review('newer-there', 700) },
        { store: 'reviews', id: 'only-there', data: review('only-there', 300) },
        { store: 'settings', id: 'main', data: { ...defaults, language: 'en', updated: 80 } },
      ],
    }),
  );

  expect(await syncNow()).toBe(true);

  const [path, init] = fetchMock.mock.calls[0] as [string, RequestInit];
  expect(path).toBe('/api/sync');
  expect((init.headers as Headers).get('Authorization')).toBe('Bearer access');
  const sent = JSON.parse(init.body as string) as {
    attempts: Attempt[];
    records: { store: string; id: string; version: number }[];
  };
  expect(sent.attempts.map((a) => a.id)).toEqual(['local']);
  expect(sent.records).toContainEqual(expect.objectContaining({ store: 'settings', version: 50 }));
  expect(sent.records).toContainEqual(
    expect.objectContaining({ store: 'reviews', id: 'newer-here', version: 900 }),
  );

  expect((await db.attempts.toCollection().primaryKeys()).sort()).toEqual([
    'local',
    'other-device',
  ]);
  expect((await db.reviews.get('newer-here'))?.lastReviewed).toBe(900);
  expect((await db.reviews.get('newer-there'))?.lastReviewed).toBe(700);
  expect(await db.reviews.get('only-there')).toBeDefined();
  expect((await db.settings.get('main'))?.language).toBe('en');
  expect(useSync.getState()).toMatchObject({ status: 'idle', lastSynced: expect.any(Number) });
});

it('changes nothing when the account returns invalid data', async () => {
  await db.reviews.add(review('w1', 100));
  fetchMock.mockResolvedValueOnce(
    json({
      attempts: [attempt('remote')],
      records: [{ store: 'reviews', id: 'w1', data: { id: 'w1', lastReviewed: 'soon' } }],
    }),
  );

  expect(await syncNow()).toBe(false);
  expect(await db.attempts.count()).toBe(0);
  expect((await db.reviews.get('w1'))?.lastReviewed).toBe(100);
  expect(useSync.getState().status).toBe('error');
});

it('reports offline and rejected syncs without throwing', async () => {
  fetchMock.mockRejectedValueOnce(new TypeError('offline'));
  expect(await syncNow()).toBe(false);
  fetchMock.mockResolvedValueOnce(json({ title: 'bad' }, 400));
  expect(await syncNow()).toBe(false);
  expect(useSync.getState().status).toBe('error');
});

it('reads server points after a sync and keeps them when the read fails', async () => {
  fetchMock
    .mockResolvedValueOnce(json({ attempts: [], records: [] }))
    .mockResolvedValueOnce(json({ total: 42, today: 12, dailyCap: 300 }));
  expect(await syncNow()).toBe(true);
  expect(fetchMock.mock.calls[1][0]).toBe('/api/points');
  expect(useSync.getState().points).toEqual({ total: 42, today: 12, dailyCap: 300 });

  fetchMock
    .mockResolvedValueOnce(json({ attempts: [], records: [] }))
    .mockResolvedValueOnce(json({ total: 'many' }));
  expect(await syncNow()).toBe(true);
  expect(useSync.getState().points?.total).toBe(42);
});

describe('auto sync', () => {
  const syncCalls = () => fetchMock.mock.calls.filter(([path]) => path === '/api/sync').length;
  let stop: () => void;
  afterEach(() => stop());

  it('syncs once shortly after new attempts while signed in', async () => {
    useAuth.setState({ email: 'learner@example.test' });
    // The account returns an attempt from another device; adding it must not start another sync.
    fetchMock.mockImplementation((path: string) =>
      Promise.resolve(
        path === '/api/sync'
          ? json({ attempts: [attempt('other-device')], records: [] })
          : json({ total: 3, today: 3, dailyCap: 300 }),
      ),
    );
    stop = startAutoSync(10);
    await logAttempt('vocabulary', 100, Date.now(), 'word');
    await logAttempt('vocabulary', 50, Date.now(), 'word');

    await vi.waitFor(() => expect(useSync.getState().points?.total).toBe(3));
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(syncCalls()).toBe(1);
    expect(await db.attempts.count()).toBe(3);
  });

  it('syncs when the connection comes back', async () => {
    useAuth.setState({ email: 'learner@example.test' });
    fetchMock.mockImplementation((path: string) =>
      Promise.resolve(
        path === '/api/sync'
          ? json({ attempts: [], records: [] })
          : json({ total: 1, today: 1, dailyCap: 300 }),
      ),
    );
    stop = startAutoSync(10);
    window.dispatchEvent(new Event('online'));
    await vi.waitFor(() => expect(syncCalls()).toBe(1));
  });

  it('stays offline-only when signed out', async () => {
    stop = startAutoSync(10);
    await logAttempt('vocabulary', 100, Date.now(), 'word');
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
