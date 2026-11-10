import { useEffect, useState } from 'react';
import { Link, NavLink, Navigate, useSearchParams } from 'react-router-dom';
import ContentManager from './ContentManager';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { ApiError, logout, useAuth } from '../../services/auth';
import {
  fetchOverview,
  fetchUsers,
  hideFromLeaderboard,
  refreshAdmin,
  setLocked,
  useAdmin,
  type AdminUser,
  type Overview,
} from '../../services/admin';

/*
THESIS: a control room whose spine is time. The online/offline split is the first thing read, then
every account hangs on one line ordered by when it was last seen: online now, today, this week,
earlier, never. Refuses the KPI-tile wall above a flat user table.
OWN-WORLD: the app's wayfinding signage; online is the green go-light, the "you are here" yellow
marks the admin's own row, 12px plates and 1px rules, no shadows.
STORY: the admin sees who is online, how much the system was used today, finds an account and acts on it.
FIRST VIEWPORT: the split bar with both counts and the refresh time, today's activity in one line of
plates, then the spine starting at "Online now".
FORM: structure #3 of 6 (control room), "timeline as spine" composition, surface roll seed 27a71f5c/0.
FINISH: critique pass in light, dark and 375px, then DESIGN.md.
*/

const REFRESH_MS = 30_000;
type Band = 'online' | 'today' | 'week' | 'older' | 'never';

function bandOf(user: AdminUser, now: number): Band {
  if (user.online) return 'online';
  if (!user.lastSeenAt) return 'never';
  const seen = new Date(user.lastSeenAt);
  if (seen.toDateString() === new Date(now).toDateString()) return 'today';
  return now - +seen < 7 * 86_400_000 ? 'week' : 'older';
}

export default function Admin() {
  const bi = useBi();
  const locale = useApp((state) => (state.settings.language === 'vi' ? 'vi-VN' : 'en-US'));
  const email = useAuth((state) => state.email);
  const { isAdmin, checkedFor } = useAdmin();
  const [params] = useSearchParams();
  const tab = params.get('tab') === 'content' ? 'content' : 'overview';
  const [overview, setOverview] = useState<Overview | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [search, setSearch] = useState('');
  const [error, setError] = useState<number | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [confirming, setConfirming] = useState<string | null>(null);

  async function load(term = search) {
    try {
      const [o, u] = await Promise.all([fetchOverview(), fetchUsers(term)]);
      setOverview(o);
      setUsers(u);
      setError(null);
    } catch (e) {
      setError(e instanceof ApiError ? e.status : 0);
    }
  }

  // Refresh on a timer so the online count stays live; searching reloads after a short pause.
  useEffect(() => {
    if (!email || !isAdmin || checkedFor !== email || tab === 'content') return;
    const pause = setTimeout(() => void load(search), 300);
    const timer = setInterval(() => void load(search), REFRESH_MS);
    return () => {
      clearTimeout(pause);
      clearInterval(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [email, isAdmin, checkedFor, search, tab]);

  // Signed out: sign in first. A learner account belongs in the learning app, not here.
  if (!email) return <Navigate to="/login?next=/admin" replace />;
  if (checkedFor !== email)
    return (
      <AdminShell>
        <p role="status">{bi('Đang kiểm tra quyền…', 'Checking access…')}</p>
      </AdminShell>
    );
  if (!isAdmin) return <Navigate to="/" replace />;
  if (tab === 'content')
    return (
      <AdminShell>
        <ContentManager />
      </AdminShell>
    );

  async function act(user: AdminUser, action: () => Promise<void>) {
    setBusy(user.id);
    setConfirming(null);
    try {
      await action();
      await load();
    } catch (e) {
      setError(e instanceof ApiError ? e.status : 0);
    } finally {
      setBusy(null);
    }
  }

  const now = overview ? Date.parse(overview.at) : Date.now();
  const relative = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
  const lastSeen = (iso?: string | null) => {
    if (!iso) return bi('Chưa mở app', 'Never opened');
    const minutes = Math.round((Date.parse(iso) - now) / 60_000);
    if (minutes > -60) return relative.format(minutes, 'minute');
    if (minutes > -24 * 60) return relative.format(Math.round(minutes / 60), 'hour');
    return new Date(iso).toLocaleDateString(locale, {
      day: 'numeric',
      month: 'numeric',
      year: 'numeric',
    });
  };
  const bands: { id: Band; name: string }[] = [
    { id: 'online', name: bi('Đang online', 'Online now') },
    { id: 'today', name: bi('Hôm nay', 'Today') },
    { id: 'week', name: bi('7 ngày qua', 'Last 7 days') },
    { id: 'older', name: bi('Lâu hơn', 'Earlier') },
    { id: 'never', name: bi('Chưa mở app từ khi có theo dõi', 'Not seen since tracking began') },
  ];
  const share = overview && overview.users ? (overview.online / overview.users) * 100 : 0;

  return (
    <AdminShell>
      <PageTitle
        title={bi('Quản trị hệ thống', 'System admin')}
        description={bi(
          'Người dùng, hiện diện và hoạt động của EnglishUp.',
          'Users, presence and activity across EnglishUp.',
        )}
      />
      {error !== null && (
        <Notice error>
          {error === 403
            ? bi('Tài khoản này không còn quyền quản trị.', 'This account is no longer an admin.')
            : bi(
                'Không tải được dữ liệu quản trị. Hãy kiểm tra máy chủ rồi thử lại.',
                'Could not load admin data. Check the server and try again.',
              )}
        </Notice>
      )}
      {overview && (
        <>
          <section className="admin-presence" aria-labelledby="presence-title">
            <div className="admin-presence-head">
              <h2 id="presence-title" className="admin-heading">
                <span className="line-tile small" aria-hidden="true">
                  <SkillIcon skill="user" size={16} />
                </span>
                {bi('Hiện diện', 'Presence')}
              </h2>
              <p className="muted">
                {bi('Cập nhật lúc', 'Updated at')}{' '}
                {new Date(overview.at).toLocaleTimeString(locale)} ·{' '}
                {bi(
                  `online = mở app trong ${overview.onlineWindowSeconds / 60} phút gần nhất`,
                  `online = app open in the last ${overview.onlineWindowSeconds / 60} minutes`,
                )}
              </p>
              <button type="button" onClick={() => void load()}>
                <SkillIcon skill="sync" size={18} />
                {bi('Làm mới', 'Refresh')}
              </button>
            </div>
            <div className="admin-split">
              <p className="admin-count online">
                <span className="admin-light" aria-hidden="true" />
                <strong>{overview.online}</strong> {bi('đang online', 'online')}
              </p>
              <p className="admin-count">
                <strong>{overview.offline}</strong> {bi('offline', 'offline')}
              </p>
            </div>
            <div
              className="admin-bar"
              role="img"
              aria-label={bi(
                `${overview.online} trên ${overview.users} tài khoản đang online`,
                `${overview.online} of ${overview.users} accounts online`,
              )}
            >
              <span style={{ width: `${share}%` }} />
            </div>
          </section>

          <section className="admin-today" aria-labelledby="today-title">
            <h2 id="today-title" className="admin-heading">
              <span className="line-tile small" aria-hidden="true">
                <SkillIcon skill="dashboard" size={16} />
              </span>
              {bi('Hôm nay', 'Today')}
            </h2>
            {/* Each figure keeps one colour, so the four read apart at a glance. */}
            <dl>
              {(
                [
                  [bi('Mở app hôm nay', 'Opened the app'), overview.activeToday, 'reading', 'user'],
                  [
                    bi('Lượt luyện tập', 'Practices'),
                    overview.attemptsToday,
                    'vocabulary',
                    'check',
                  ],
                  [
                    bi('Câu hỏi trợ giảng', 'Tutor questions'),
                    overview.questionsToday,
                    'listening',
                    'assistant',
                  ],
                  [bi('Ván Đua 60 giây', 'Races'), overview.gamesToday, 'speaking', 'game'],
                ] as const
              ).map(([label, value, skill, icon]) => (
                <div key={label} data-skill={skill}>
                  <dt>
                    <span className="line-tile small" aria-hidden="true">
                      <SkillIcon skill={icon} size={16} />
                    </span>
                    {label}
                  </dt>
                  <dd>{value}</dd>
                </div>
              ))}
            </dl>
            <p className="muted">
              {bi(
                `${overview.users} tài khoản · ${overview.admins} quản trị viên · ${overview.locked} bị khoá · ${overview.knowledgeChunks} đoạn nội dung cho trợ giảng`,
                `${overview.users} accounts · ${overview.admins} admins · ${overview.locked} locked · ${overview.knowledgeChunks} content chunks for the tutor`,
              )}
            </p>
          </section>
        </>
      )}

      <section className="admin-users" aria-labelledby="users-title">
        <div className="admin-users-head">
          <h2 id="users-title" className="admin-heading">
            <span className="line-tile small" aria-hidden="true">
              <SkillIcon skill="admin" size={16} />
            </span>
            {bi('Người dùng', 'Users')}
          </h2>
          <label>
            <span className="sr-only">{bi('Tìm người dùng', 'Search users')}</span>
            <input
              type="search"
              placeholder={bi(
                'Tìm theo email hoặc tên hiển thị',
                'Search by email or display name',
              )}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </label>
        </div>
        {bands.map((band) => {
          const members = users.filter((u) => bandOf(u, now) === band.id);
          if (!members.length) return null;
          return (
            <section key={band.id} className={`admin-band ${band.id}`} aria-label={band.name}>
              <h3>
                {band.name} <span>{members.length}</span>
              </h3>
              <ol>
                {members.map((u) => {
                  const self = u.email === email;
                  return (
                    <li key={u.id} className={self ? 'self' : undefined}>
                      <span
                        className={u.online ? 'admin-light' : 'admin-light off'}
                        aria-hidden="true"
                      />
                      <div className="admin-who">
                        <strong>{u.email}</strong>
                        <small>
                          {u.displayName ?? bi('Chưa có hồ sơ', 'No profile yet')}
                          {u.isAdmin && <em className="admin-tag">{bi('Quản trị', 'Admin')}</em>}
                          {u.locked && (
                            <em className="admin-tag locked">{bi('Bị khoá', 'Locked')}</em>
                          )}
                          {u.showOnLeaderboard && (
                            <em className="admin-tag">
                              {bi('Trên bảng xếp hạng', 'On leaderboard')}
                            </em>
                          )}
                        </small>
                      </div>
                      <p className="admin-facts">
                        <span>
                          {u.points} {bi('điểm', 'pts')} · {u.attempts} {bi('lượt', 'practices')}
                        </span>
                        <span>
                          {u.online ? bi('Đang online', 'Online now') : lastSeen(u.lastSeenAt)}
                        </span>
                      </p>
                      <div className="admin-actions">
                        {u.showOnLeaderboard && (
                          <button
                            type="button"
                            disabled={busy === u.id}
                            onClick={() => void act(u, () => hideFromLeaderboard(u.id))}
                          >
                            <SkillIcon skill="eyeOff" size={16} />
                            {bi('Ẩn khỏi bảng xếp hạng', 'Hide from leaderboard')}
                          </button>
                        )}
                        {!self &&
                          (u.locked ? (
                            <button
                              type="button"
                              disabled={busy === u.id}
                              onClick={() => void act(u, () => setLocked(u.id, false))}
                            >
                              <SkillIcon skill="lock" size={16} />
                              {bi('Mở khoá', 'Unlock')}
                            </button>
                          ) : confirming === u.id ? (
                            <button
                              type="button"
                              className="danger"
                              disabled={busy === u.id}
                              onClick={() => void act(u, () => setLocked(u.id, true))}
                            >
                              <SkillIcon skill="lock" size={16} />
                              {bi('Xác nhận khoá', 'Confirm lock')}
                            </button>
                          ) : (
                            <button
                              type="button"
                              className="danger-outline"
                              onClick={() => setConfirming(u.id)}
                            >
                              <SkillIcon skill="lock" size={16} />
                              {bi('Khoá tài khoản', 'Lock account')}
                            </button>
                          ))}
                      </div>
                    </li>
                  );
                })}
              </ol>
            </section>
          );
        })}
        {overview && !users.length && (
          <p className="muted">{bi('Không có người dùng phù hợp.', 'No matching users.')}</p>
        )}
      </section>
    </AdminShell>
  );
}

/** The admin area's own frame: a sign-blue bar with the admin's email, a way back to learning and sign out. */
function AdminShell({ children }: { children: React.ReactNode }) {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const checkedFor = useAdmin((state) => state.checkedFor);
  const tabParam = useSearchParams()[0].get('tab');
  // Opening /admin directly (or after a reload) checks the role here; the learning shell is not mounted.
  useEffect(() => {
    if (email && checkedFor !== email) void refreshAdmin();
  }, [email, checkedFor]);
  return (
    <div className="admin-shell">
      <a className="skip" href="#main">
        Skip to content / Đến nội dung
      </a>
      <header className="admin-top">
        <Link className="admin-brand" to="/admin">
          <span className="brand-mark" aria-hidden="true">
            e<span>↗</span>
          </span>
          EnglishUp
          <span className="admin-badge">{bi('Quản trị', 'Admin')}</span>
        </Link>
        <nav className="admin-nav" aria-label={bi('Khu quản trị', 'Admin areas')}>
          <NavLink
            to="/admin"
            end
            className={({ isActive }) => (isActive && !tabParam ? 'active' : '')}
          >
            {bi('Tổng quan', 'Overview')}
          </NavLink>
          <NavLink
            to="/admin?tab=content"
            className={() => (tabParam === 'content' ? 'active' : '')}
          >
            {bi('Tài liệu học tập', 'Learning content')}
          </NavLink>
        </nav>
        <div className="admin-top-actions">
          {email && <span className="admin-top-email">{email}</span>}
          <Link className="button" to="/">
            {bi('Trang học tập', 'Learning app')}
          </Link>
          {email && (
            <button type="button" onClick={logout}>
              <SkillIcon skill="logout" size={18} />
              {bi('Đăng xuất', 'Sign out')}
            </button>
          )}
        </div>
      </header>
      <main id="main" className="admin-main" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
