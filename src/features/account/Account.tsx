import { useEffect, useState } from 'react';
import { Link, Navigate, useSearchParams } from 'react-router-dom';
import { useBi, useT } from '../../i18n';
import { Notice, PageTitle, useLive } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { AuthError, changePassword, logout, useAuth } from '../../services/auth';
import { syncNow, useSync } from '../../services/sync';
import { db } from '../../services/storage';
import { dayKey } from '../../services/srs';
import { getProgress, skills } from '../../services/progress';
import {
  fetchAchievements,
  fetchLeaderboard,
  fetchProfile,
  saveProfile,
  type Achievement,
  type Profile,
} from '../../services/community';
import { badgeText } from '../achievements/Achievements';
import { PasswordRules, passwordRules } from './SignIn';

/*
Brief: the user's reference is a classic account-settings page (profile card and section menu on the
left, the chosen section's form on the right). That convention is played straight, dressed in the
app's wayfinding world: a sign-blue cover on the card, a yellow monogram, menu rows like the sidebar
directory (tile, label, chevron; the current one tinted with the yellow dot). Only sections the
product really has: profile, points and sync, journey, password, privacy, sign out.
*/

type Tab = 'profile' | 'points' | 'journey' | 'password' | 'privacy';
type Day = { time: number; skills: Set<string>; count: number; seconds: number; badges: string[] };

const initial = (name: string) => (name.trim()[0] ?? '?').toUpperCase();

export default function Account() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const [params] = useSearchParams();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [profileError, setProfileError] = useState(false);

  useEffect(() => {
    if (!email) return;
    let current = true;
    fetchProfile()
      .then((loaded) => current && setProfile(loaded))
      .catch(() => current && setProfileError(true));
    return () => {
      current = false;
    };
  }, [email]);

  // Signed-out learners sign in on the full-screen entrance and come back here.
  if (!email) return <Navigate to="/login?next=/account" replace />;

  const sections: { id: Tab; icon: IconName; label: string }[] = [
    { id: 'profile', icon: 'user', label: bi('Hồ sơ', 'Profile') },
    { id: 'points', icon: 'sync', label: bi('Điểm & đồng bộ', 'Points & sync') },
    { id: 'journey', icon: 'streak', label: bi('Hành trình học', 'Learning journey') },
    { id: 'password', icon: 'lock', label: bi('Đổi mật khẩu', 'Change password') },
    { id: 'privacy', icon: 'shield', label: bi('Quyền riêng tư', 'Privacy') },
  ];
  const tab = sections.find((s) => s.id === params.get('tab')) ?? sections[0];
  const name = profile?.displayName.trim();

  return (
    <>
      <PageTitle title={bi('Tài khoản', 'Account')} />
      <div className="account">
        <aside className="account-side">
          <div className="account-card">
            <span className="account-cover" aria-hidden="true" />
            <span className="account-avatar" aria-hidden="true">
              {initial(name || email)}
            </span>
            <strong className="account-name">{name || email}</strong>
            {name && <small className="account-email">{email}</small>}
            <Link className="account-view" to="/achievements">
              {bi('Xem thành tích', 'View achievements')}
              <SkillIcon skill="arrow" size={16} />
            </Link>
          </div>
          <nav className="account-menu" aria-label={bi('Mục tài khoản', 'Account sections')}>
            <ul>
              {sections.map((s) => (
                <li key={s.id}>
                  <Link
                    to={`?tab=${s.id}`}
                    replace
                    aria-current={s.id === tab.id ? 'page' : undefined}
                  >
                    <span className="account-menu-tile" aria-hidden="true">
                      <SkillIcon skill={s.icon} size={18} />
                    </span>
                    {s.label}
                    <SkillIcon skill="chevron" size={16} />
                  </Link>
                </li>
              ))}
              <li>
                <button type="button" onClick={logout}>
                  <span className="account-menu-tile" aria-hidden="true">
                    <SkillIcon skill="logout" size={18} />
                  </span>
                  {bi('Đăng xuất', 'Sign out')}
                </button>
              </li>
            </ul>
          </nav>
        </aside>

        <section className="account-pane" aria-labelledby="account-pane-title">
          <h2 id="account-pane-title">
            <SkillIcon skill={tab.icon} size={22} />
            {tab.label}
          </h2>
          {tab.id === 'profile' &&
            (profile ? (
              <ProfileSection email={email} profile={profile} setProfile={setProfile} />
            ) : profileError ? (
              <Notice error>{bi('Không tải được hồ sơ.', 'Could not load your profile.')}</Notice>
            ) : (
              <p className="muted">{bi('Đang tải hồ sơ…', 'Loading your profile…')}</p>
            ))}
          {tab.id === 'points' && <PointsSection />}
          {tab.id === 'journey' && <JourneySection />}
          {tab.id === 'password' && <PasswordSection />}
          {tab.id === 'privacy' && <PrivacySection />}
        </section>
      </div>
    </>
  );
}

/** Email (read only), display name and leaderboard opt-in, with a live preview of the public row. */
function ProfileSection({
  email,
  profile,
  setProfile,
}: {
  email: string;
  profile: Profile;
  setProfile: (profile: Profile) => void;
}) {
  const bi = useBi();
  const { points, lastSynced } = useSync();
  const [state, setState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [rank, setRank] = useState<number | null>(null);

  useEffect(() => {
    let current = true;
    fetchLeaderboard('all')
      .then((board) => current && setRank(board.entries.find((e) => e.isMe)?.rank ?? null))
      .catch(() => undefined);
    return () => {
      current = false;
    };
  }, [lastSynced]);

  return (
    <form
      className="account-form"
      onSubmit={(event) => {
        event.preventDefault();
        setState('saving');
        saveProfile(profile)
          .then((saved) => {
            setProfile(saved);
            setState('saved');
          })
          .catch(() => setState('error'));
      }}
    >
      <label>
        Email
        <input type="email" value={email} readOnly aria-describedby="email-note" />
        <small id="email-note">
          {bi('Dùng để đăng nhập; không ai khác thấy.', 'Used to sign in; nobody else sees it.')}
        </small>
      </label>
      <label>
        {bi('Tên hiển thị', 'Display name')}
        <input
          required
          minLength={2}
          maxLength={40}
          value={profile.displayName}
          onChange={(e) => {
            setProfile({ ...profile, displayName: e.target.value });
            setState('idle');
          }}
        />
      </label>
      <label className="checkbox">
        <input
          type="checkbox"
          checked={profile.showOnLeaderboard}
          onChange={(e) => {
            setProfile({ ...profile, showOnLeaderboard: e.target.checked });
            setState('idle');
          }}
        />
        {bi(
          'Hiện tôi trên bảng xếp hạng (chỉ tên hiển thị và điểm, không hiện email)',
          'Show me on the leaderboard (display name and points only, never my email)',
        )}
      </label>
      <figure className="profile-preview">
        {profile.showOnLeaderboard ? (
          <div className="profile-row">
            <span className="profile-rank">{rank ?? '–'}</span>
            <span className="profile-monogram" aria-hidden="true">
              {initial(profile.displayName)}
            </span>
            <strong>{profile.displayName.trim() || '…'}</strong>
            <span className="profile-points">
              {points?.total ?? 0} {bi('điểm', 'pts')}
            </span>
          </div>
        ) : (
          <div className="profile-row hidden">
            <SkillIcon skill="eyeOff" size={20} />
            {bi('Bạn đang ẩn khỏi bảng xếp hạng.', 'You are hidden from the leaderboard.')}
          </div>
        )}
        <figcaption>
          {bi(
            'Xem trước hàng của bạn trên bảng xếp hạng mọi thời gian.',
            'A preview of your all-time leaderboard row.',
          )}
        </figcaption>
      </figure>
      {state === 'saved' && <p role="status">{bi('Đã lưu hồ sơ.', 'Profile saved.')}</p>}
      {state === 'error' && (
        <Notice error>
          {bi(
            'Không lưu được. Tên hiển thị cần 2–40 ký tự; hãy kiểm tra kết nối.',
            'Could not save. Display names need 2–40 characters; check your connection.',
          )}
        </Notice>
      )}
      <div className="actions">
        <button className="primary" disabled={state === 'saving'}>
          {bi('Lưu hồ sơ', 'Save profile')}
        </button>
      </div>
    </form>
  );
}

/** The score plate (total, today against the cap, streak) and syncing. */
function PointsSection() {
  const bi = useBi();
  const locale = useApp((state) => (state.settings.language === 'vi' ? 'vi-VN' : 'en-US'));
  const { status, lastSynced, points } = useSync();
  const { value: attempts = [] } = useLive(() => db.attempts.toArray());
  const { streak } = getProgress(attempts);
  const cap = points?.dailyCap ?? 300;
  return (
    <>
      <div className="profile-plate">
        <dl className="profile-score">
          <div>
            <dt>{bi('Tổng điểm', 'Total points')}</dt>
            <dd>{points?.total ?? '–'}</dd>
          </div>
          <div>
            <dt>{bi('Điểm hôm nay', 'Points today')}</dt>
            <dd>
              {points?.today ?? 0}
              <small> / {cap}</small>
            </dd>
            <progress
              value={points?.today ?? 0}
              max={cap}
              aria-label={bi('Điểm hôm nay', 'Points today')}
            />
          </div>
          <div>
            <dt>{bi('Chuỗi ngày', 'Day streak')}</dt>
            <dd>{streak}</dd>
          </div>
        </dl>
        <p className="profile-small">
          {bi(
            `Mỗi lượt luyện tập được 1–5 điểm theo kết quả, tối đa ${cap} điểm mỗi ngày; máy chủ tính điểm sau khi đồng bộ.`,
            `Each practice earns 1–5 points by result, up to ${cap} a day; the server awards them after syncing.`,
          )}
        </p>
      </div>
      <div className="account-sync">
        <p role="status">
          {status === 'syncing'
            ? bi('Đang đồng bộ…', 'Syncing…')
            : lastSynced
              ? `${bi('Đồng bộ lần cuối', 'Last synced')}: ${new Date(lastSynced).toLocaleTimeString(locale)}`
              : bi('Chưa đồng bộ trong phiên này.', 'Not synced in this session.')}
        </p>
        <button className="primary" disabled={status === 'syncing'} onClick={() => void syncNow()}>
          {bi('Đồng bộ ngay', 'Sync now')}
        </button>
      </div>
      {status === 'error' && (
        <Notice error>
          {bi(
            'Không đồng bộ được. Dữ liệu trên thiết bị này vẫn an toàn; hãy thử lại khi có mạng.',
            'Sync failed. Data on this device is safe; try again when you are online.',
          )}
        </Notice>
      )}
      <p className="muted">
        {bi(
          'Tiến độ được gộp giữa thiết bị này và tài khoản khi mở ứng dụng, sau mỗi lượt luyện tập hoặc khi bấm Đồng bộ. Xoá từ hay đặt lại dữ liệu chỉ có tác dụng trên thiết bị này.',
          'Progress merges between this device and your account when the app opens, after each practice or when you select Sync. Deleting words or resetting data only affects this device.',
        )}
      </p>
    </>
  );
}

/** The last active days as stops on a route, in skill-line colours, with badge days marked. */
function JourneySection() {
  const bi = useBi();
  const t = useT();
  const locale = useApp((state) => (state.settings.language === 'vi' ? 'vi-VN' : 'en-US'));
  const { lastSynced } = useSync();
  const { value: attempts = [] } = useLive(() => db.attempts.toArray());
  const [badges, setBadges] = useState<Achievement[]>([]);

  useEffect(() => {
    let current = true;
    fetchAchievements()
      .then((list) => current && setBadges(list.filter((b) => b.earnedAt)))
      .catch(() => undefined);
    return () => {
      current = false;
    };
  }, [lastSynced]);

  const days = new Map<string, Day>();
  const day = (time: number) => {
    const key = dayKey(time);
    if (!days.has(key))
      days.set(key, { time, skills: new Set(), count: 0, seconds: 0, badges: [] });
    return days.get(key)!;
  };
  for (const a of attempts) {
    const d = day(a.timestamp);
    d.skills.add(a.skill);
    d.count++;
    d.seconds += a.duration;
  }
  for (const b of badges) day(Date.parse(b.earnedAt!)).badges.push(b.code);
  const journey = [...days.values()].sort((a, b) => b.time - a.time).slice(0, 10);

  if (!journey.length)
    return (
      <p className="muted">
        {bi(
          'Chưa có buổi học nào trên thiết bị này. Hoàn thành một bài để bắt đầu hành trình.',
          'No sessions on this device yet. Finish a lesson to start your journey.',
        )}
      </p>
    );
  return (
    <ol className="journey">
      {journey.map((d) => (
        <li key={dayKey(d.time)} className={d.badges.length ? 'milestone' : undefined}>
          <span className="journey-dot" aria-hidden="true" />
          <time dateTime={dayKey(d.time)}>
            {new Date(d.time).toLocaleDateString(locale, {
              weekday: 'short',
              day: 'numeric',
              month: 'numeric',
            })}
          </time>
          <div className="journey-body">
            {d.count > 0 && (
              <p>
                <span className="journey-lines">
                  {skills
                    .filter((s) => d.skills.has(s))
                    .map((s) => (
                      <span key={s} className="line-tile small" data-skill={s} title={t(s)}>
                        <SkillIcon skill={s} size={16} />
                        <span className="sr-only">{t(s)}</span>
                      </span>
                    ))}
                </span>
                {bi(`${d.count} lượt`, `${d.count} practices`)} ·{' '}
                {Math.max(1, Math.round(d.seconds / 60))} {t('minutes')}
              </p>
            )}
            {d.badges.map((code) => (
              <p key={code} className="journey-badge">
                <SkillIcon skill="achievements" size={16} />
                {bi('Huy hiệu', 'Badge')}:{' '}
                {bi(badgeText[code]?.[0] ?? code, badgeText[code]?.[1] ?? code)}
              </p>
            ))}
          </div>
        </li>
      ))}
    </ol>
  );
}

/** Current password, new password with the live rule list, and a confirmation. */
function PasswordSection() {
  const bi = useBi();
  const [form, setForm] = useState({ current: '', next: '', again: '' });
  const [state, setState] = useState<
    'idle' | 'saving' | 'saved' | 'invalid' | 'password' | 'network'
  >('idle');
  const mismatch = form.again !== '' && form.again !== form.next;
  const ready = passwordRules.every((rule) => rule.test(form.next)) && !mismatch && form.current;
  const messages = {
    invalid: bi('Mật khẩu hiện tại không đúng.', 'The current password is incorrect.'),
    password: bi(
      'Mật khẩu mới chưa đủ các điều kiện bên dưới.',
      'The new password does not meet the rules below.',
    ),
    network: bi(
      'Không kết nối được máy chủ. Mật khẩu chưa đổi; hãy thử lại khi có mạng.',
      'Cannot reach the server. The password is unchanged; try again when you are online.',
    ),
  };
  return (
    <form
      className="account-form"
      onSubmit={(event) => {
        event.preventDefault();
        if (!ready) return;
        setState('saving');
        changePassword(form.current, form.next)
          .then(() => {
            setForm({ current: '', next: '', again: '' });
            setState('saved');
          })
          .catch((e: unknown) =>
            setState(
              e instanceof AuthError && e.kind === 'invalid'
                ? 'invalid'
                : e instanceof AuthError && e.kind === 'password'
                  ? 'password'
                  : 'network',
            ),
          );
      }}
    >
      <label>
        {bi('Mật khẩu hiện tại', 'Current password')}
        <input
          type="password"
          required
          autoComplete="current-password"
          value={form.current}
          onChange={(e) => setForm({ ...form, current: e.target.value })}
        />
      </label>
      <label>
        {bi('Mật khẩu mới', 'New password')}
        <input
          type="password"
          required
          autoComplete="new-password"
          aria-describedby="new-password-rules"
          value={form.next}
          onChange={(e) => setForm({ ...form, next: e.target.value })}
        />
      </label>
      <PasswordRules id="new-password-rules" password={form.next} />
      <label>
        {bi('Nhập lại mật khẩu mới', 'Repeat the new password')}
        <input
          type="password"
          required
          autoComplete="new-password"
          aria-invalid={mismatch || undefined}
          aria-describedby={mismatch ? 'password-mismatch' : undefined}
          value={form.again}
          onChange={(e) => setForm({ ...form, again: e.target.value })}
        />
      </label>
      {mismatch && (
        <small className="account-field-error" id="password-mismatch">
          {bi('Hai mật khẩu mới chưa giống nhau.', 'The two new passwords do not match.')}
        </small>
      )}
      {state === 'saved' && <p role="status">{bi('Đã đổi mật khẩu.', 'Password changed.')}</p>}
      {(state === 'invalid' || state === 'password' || state === 'network') && (
        <Notice error>{messages[state]}</Notice>
      )}
      <div className="actions">
        <button className="primary" disabled={!ready || state === 'saving'}>
          {bi('Đổi mật khẩu', 'Change password')}
        </button>
      </div>
    </form>
  );
}

/** Where each kind of data lives and who sees it; the facts, not a settings maze. */
function PrivacySection() {
  const bi = useBi();
  const rows: { icon: IconName; title: string; text: React.ReactNode }[] = [
    {
      icon: 'dashboard',
      title: bi('Trên thiết bị này', 'On this device'),
      text: (
        <>
          {bi(
            'Bài đã học, từ đã lưu và lịch ôn nằm trong trình duyệt. Sao lưu, nhập lại hoặc xoá chúng trong',
            'Lessons, saved words and reviews live in the browser. Back them up, import or reset them in',
          )}{' '}
          <Link to="/settings">{bi('Cài đặt', 'Settings')}</Link>.
        </>
      ),
    },
    {
      icon: 'sync',
      title: bi('Trên tài khoản', 'In your account'),
      text: bi(
        'Tiến độ được đồng bộ lên máy chủ EnglishUp để dùng trên nhiều thiết bị và tính điểm. Email chỉ dùng để đăng nhập.',
        'Progress syncs to the EnglishUp server so you can use other devices and earn points. Your email is only for signing in.',
      ),
    },
    {
      icon: 'achievements',
      title: bi('Bảng xếp hạng', 'Leaderboard'),
      text: bi(
        'Chỉ hiện tên hiển thị và điểm, và chỉ khi bạn bật trong mục Hồ sơ.',
        'Shows only your display name and points, and only if you turn it on under Profile.',
      ),
    },
    {
      icon: 'assistant',
      title: bi('Trợ giảng AI', 'AI tutor'),
      text: bi(
        'Câu hỏi được gửi tới Google Gemini (gói miễn phí, Google có thể dùng để cải thiện dịch vụ). Đừng nhập thông tin cá nhân.',
        'Questions go to Google Gemini (free tier; Google may use them to improve its services). Do not enter personal information.',
      ),
    },
    {
      icon: 'speaking',
      title: bi('Ghi âm', 'Recordings'),
      text: bi(
        'Bản ghi chỉ nằm trong bộ nhớ khi bạn luyện nói, không bao giờ được lưu hay gửi lên máy chủ EnglishUp. Nếu bạn bật nhận dạng giọng nói, trình duyệt có thể gửi âm thanh tới dịch vụ của nó.',
        'Recordings stay in memory while you practise speaking and are never saved or sent to the EnglishUp server. If you turn on speech recognition, the browser may send audio to its own service.',
      ),
    },
  ];
  return (
    <dl className="account-privacy">
      {rows.map((row) => (
        <div key={row.title}>
          <dt>
            <span className="account-menu-tile" aria-hidden="true">
              <SkillIcon skill={row.icon} size={18} />
            </span>
            {row.title}
          </dt>
          <dd>{row.text}</dd>
        </div>
      ))}
    </dl>
  );
}
