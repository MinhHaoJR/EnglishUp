import { useState } from 'react';
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

export default function Account() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
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
          <p className="muted">
            {bi(
              'Tiến độ học hiện vẫn lưu trên thiết bị này. Đồng bộ với tài khoản sẽ có ở bản tiếp theo.',
              'Learning progress is still stored on this device. Account sync arrives in the next release.',
            )}
          </p>
          <button onClick={logout}>{bi('Đăng xuất', 'Sign out')}</button>
        </section>
      </>
    );

  return (
    <>
      <PageTitle
        title={bi('Tài khoản', 'Account')}
        description={bi(
          'Đăng nhập để lưu điểm, nhận thành tích và tham gia bảng xếp hạng. Không đăng nhập vẫn học được.',
          'Sign in to keep points, earn achievements and join the leaderboard. You can still practice without an account.',
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
