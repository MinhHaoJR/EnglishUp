import { useEffect, useState } from 'react';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import {
  AuthError,
  login,
  logout,
  register,
  useAuth,
  type AuthErrorKind,
} from '../../services/auth';
import { syncNow, useSync } from '../../services/sync';
import { fetchProfile, saveProfile, type Profile } from '../../services/community';

export default function Account() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const { status, lastSynced, points } = useSync();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [form, setForm] = useState({ email: '', password: '' });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<AuthErrorKind | ''>('');
  const messages: Record<AuthErrorKind, string> = {
    invalid: bi('Email hoặc mật khẩu không đúng.', 'Incorrect email or password.'),
    locked: bi(
      'Tài khoản tạm khoá do nhập sai nhiều lần. Hãy thử lại sau vài phút.',
      'Too many failed attempts. Try again in a few minutes.',
    ),
    exists: bi('Email này đã được đăng ký.', 'This email is already registered.'),
    password: bi(
      'Mật khẩu cần ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.',
      'Use at least 8 characters with upper and lower case letters, a digit and a symbol.',
    ),
    email: bi('Email không hợp lệ.', 'Enter a valid email address.'),
    network: bi(
      'Không kết nối được máy chủ EnglishUp. Việc học trên thiết bị này vẫn hoạt động.',
      'Cannot reach the EnglishUp server. Practice on this device still works.',
    ),
  };

  if (email)
    return (
      <>
        <PageTitle title={bi('Tài khoản', 'Account')} />
        <section className="panel space-y-4">
          <p>
            {bi('Đang đăng nhập với', 'Signed in as')} <strong>{email}</strong>
          </p>
          {points && (
            <div className="stats">
              <div className="stat">
                <span>{bi('Điểm hôm nay', 'Points today')}</span>
                <strong>
                  {points.today}
                  <small> / {points.dailyCap}</small>
                </strong>
                <progress
                  value={points.today}
                  max={points.dailyCap}
                  aria-label={bi('Điểm hôm nay', 'Points today')}
                />
              </div>
              <div className="stat">
                <span>{bi('Tổng điểm', 'Total points')}</span>
                <strong>{points.total}</strong>
              </div>
            </div>
          )}
          <p className="muted">
            {bi(
              `Mỗi lượt luyện tập được 1–5 điểm theo kết quả, tối đa ${points?.dailyCap ?? 300} điểm mỗi ngày; máy chủ tính điểm sau khi đồng bộ.`,
              `Each practice earns 1–5 points by result, up to ${points?.dailyCap ?? 300} a day; the server awards them after syncing.`,
            )}
          </p>
          <p className="muted">
            {bi(
              'Tiến độ học được gộp giữa thiết bị này và tài khoản mỗi khi mở ứng dụng, sau mỗi lượt luyện tập hoặc khi bấm Đồng bộ. Xoá từ hay đặt lại dữ liệu chỉ có tác dụng trên thiết bị này.',
              'Progress merges between this device and your account when the app opens, after each practice or when you select Sync. Deleting words or resetting data only affects this device.',
            )}
          </p>
          <p role="status">
            {status === 'syncing'
              ? bi('Đang đồng bộ…', 'Syncing…')
              : lastSynced
                ? `${bi('Đồng bộ lần cuối', 'Last synced')}: ${new Date(lastSynced).toLocaleTimeString()}`
                : bi('Chưa đồng bộ trong phiên này.', 'Not synced in this session.')}
          </p>
          {status === 'error' && (
            <Notice error>
              {bi(
                'Không đồng bộ được. Dữ liệu trên thiết bị này vẫn an toàn; hãy thử lại khi có mạng.',
                'Sync failed. Data on this device is safe; try again when you are online.',
              )}
            </Notice>
          )}
          <div className="actions">
            <button
              className="primary"
              disabled={status === 'syncing'}
              onClick={() => void syncNow()}
            >
              {bi('Đồng bộ ngay', 'Sync now')}
            </button>
            <button onClick={logout}>{bi('Đăng xuất', 'Sign out')}</button>
          </div>
        </section>
        <ProfileForm />
      </>
    );

  return (
    <>
      <PageTitle
        title={bi('Tài khoản', 'Account')}
        description={bi(
          'Đăng nhập để lưu tiến độ lên tài khoản và dùng trên nhiều thiết bị. Tiến độ đang có trên thiết bị này sẽ được gộp vào tài khoản. Không đăng nhập vẫn học được.',
          'Sign in to keep progress in your account across devices. Progress already on this device is merged into the account. You can still practice without an account.',
        )}
      />
      <div className="tabs">
        {(['login', 'register'] as const).map((value) => (
          <button
            key={value}
            aria-pressed={mode === value}
            onClick={() => {
              setMode(value);
              setError('');
            }}
          >
            {value === 'login' ? bi('Đăng nhập', 'Sign in') : bi('Đăng ký', 'Create account')}
          </button>
        ))}
      </div>
      <form
        className="panel form-grid"
        onSubmit={(event) => {
          event.preventDefault();
          setBusy(true);
          setError('');
          (mode === 'login' ? login : register)(form.email, form.password)
            .then(syncNow)
            .catch((e: unknown) => setError(e instanceof AuthError ? e.kind : 'network'))
            .finally(() => setBusy(false));
        }}
      >
        <label>
          Email
          <input
            type="email"
            required
            autoComplete="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </label>
        <label>
          {bi('Mật khẩu', 'Password')}
          <input
            type="password"
            required
            minLength={mode === 'register' ? 8 : undefined}
            autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </label>
        {mode === 'register' && <p className="muted">{messages.password}</p>}
        {error && <Notice error>{messages[error]}</Notice>}
        <div className="actions">
          <button className="primary" disabled={busy}>
            {mode === 'login' ? bi('Đăng nhập', 'Sign in') : bi('Tạo tài khoản', 'Create account')}
          </button>
        </div>
      </form>
    </>
  );
}

/** Display name and leaderboard opt-in; the leaderboard never shows emails. */
function ProfileForm() {
  const bi = useBi();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [state, setState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  useEffect(() => {
    let current = true;
    fetchProfile()
      .then((loaded) => current && setProfile(loaded))
      .catch(() => current && setState('error'));
    return () => {
      current = false;
    };
  }, []);

  if (!profile)
    return state === 'error' ? (
      <Notice error>{bi('Không tải được hồ sơ.', 'Could not load your profile.')}</Notice>
    ) : null;

  return (
    <form
      className="panel space-y-4"
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
      <h2>{bi('Hồ sơ trên bảng xếp hạng', 'Leaderboard profile')}</h2>
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
