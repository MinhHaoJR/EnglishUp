import { useState } from 'react';
import { Link, Navigate, useSearchParams } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { AuthError, login, register, useAuth, type AuthErrorKind } from '../../services/auth';
import { syncNow } from '../../services/sync';

/** Only same-site paths, so a crafted link cannot send a learner to another site after signing in. */
export function safeNext(raw: string | null) {
  return raw?.startsWith('/') && !raw.startsWith('//') && !raw.startsWith('/login') ? raw : '/';
}

/** The server's Identity rules (ASP.NET defaults plus 8 characters), shown live while creating an account. */
export const passwordRules = [
  { test: (p: string) => p.length >= 8, vi: 'Ít nhất 8 ký tự', en: 'At least 8 characters' },
  { test: (p: string) => /[a-z]/.test(p), vi: 'Một chữ thường', en: 'A lower-case letter' },
  { test: (p: string) => /[A-Z]/.test(p), vi: 'Một chữ hoa', en: 'An upper-case letter' },
  { test: (p: string) => /\d/.test(p), vi: 'Một chữ số', en: 'A digit' },
  { test: (p: string) => /[^a-zA-Z0-9]/.test(p), vi: 'Một ký tự đặc biệt', en: 'A symbol' },
];

/**
 * The station entrance: a sign-blue plate saying what an account adds, beside the form.
 * Lives outside the app shell; practice never needs it.
 */
export default function SignIn() {
  const bi = useBi();
  const [params] = useSearchParams();
  const next = safeNext(params.get('next'));
  const email = useAuth((state) => state.email);
  const [mode, setMode] = useState<'login' | 'register'>(
    params.get('mode') === 'register' ? 'register' : 'login',
  );
  const [form, setForm] = useState({ email: '', password: '' });
  const [reveal, setReveal] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<AuthErrorKind | ''>('');

  if (email) return <Navigate to={next} replace />;

  const messages: Record<AuthErrorKind, string> = {
    invalid: bi(
      'Email hoặc mật khẩu không đúng. Kiểm tra lại, hoặc tạo tài khoản nếu bạn chưa có.',
      'Incorrect email or password. Check them, or create an account if you have none.',
    ),
    locked: bi(
      'Tài khoản tạm khoá do nhập sai nhiều lần. Hãy thử lại sau vài phút.',
      'Too many failed attempts. Try again in a few minutes.',
    ),
    exists: bi(
      'Email này đã có tài khoản. Hãy chuyển sang Đăng nhập.',
      'This email already has an account. Switch to Sign in.',
    ),
    password: bi(
      'Mật khẩu chưa đủ các điều kiện bên dưới.',
      'The password does not meet the rules below.',
    ),
    email: bi('Email không hợp lệ.', 'Enter a valid email address.'),
    network: bi(
      'Không kết nối được máy chủ EnglishUp. Bài học trên thiết bị này vẫn dùng được; hãy thử lại khi có mạng.',
      'Cannot reach the EnglishUp server. Lessons on this device still work; try again when you are online.',
    ),
  };
  const creating = mode === 'register';
  const stops = [
    {
      icon: 'sync' as const,
      text: bi(
        'Đồng bộ tiến độ giữa điện thoại và máy tính',
        'Sync progress between phone and computer',
      ),
    },
    {
      icon: 'achievements' as const,
      text: bi(
        'Nhận điểm, huy hiệu và lên bảng xếp hạng',
        'Earn points and badges, join the leaderboard',
      ),
    },
    {
      icon: 'assistant' as const,
      text: bi(
        'Hỏi trợ giảng AI và chơi Đua 60 giây',
        'Ask the AI tutor and play the 60-second race',
      ),
    },
  ];

  return (
    <div className="signin">
      <section className="signin-sign" aria-labelledby="signin-title">
        <Link className="signin-brand" to="/">
          <span className="brand-mark" aria-hidden="true">
            e<span>↗</span>
          </span>
          EnglishUp
        </Link>
        <h1 id="signin-title">{bi('Mang tiến độ học theo bạn', 'Take your progress with you')}</h1>
        <ol className="signin-stops">
          {stops.map((stop) => (
            <li key={stop.icon}>
              <span className="signin-stop-tile" aria-hidden="true">
                <SkillIcon skill={stop.icon} />
              </span>
              {stop.text}
            </li>
          ))}
        </ol>
        <p className="signin-free">
          {bi(
            'Không cần tài khoản để học: mọi bài vẫn lưu trên thiết bị này.',
            'No account is needed to practise: every lesson saves on this device.',
          )}
        </p>
      </section>

      <section className="signin-panel">
        <div className="tabs" aria-label={bi('Chọn cách vào', 'Choose how to continue')}>
          {(['login', 'register'] as const).map((value) => (
            <button
              key={value}
              type="button"
              aria-pressed={mode === value}
              onClick={() => {
                setMode(value);
                setError('');
              }}
            >
              {value === 'login'
                ? bi('Đăng nhập', 'Sign in')
                : bi('Tạo tài khoản', 'Create account')}
            </button>
          ))}
        </div>
        <h2>
          {creating
            ? bi('Bắt đầu lưu tiến độ', 'Start saving your progress')
            : bi('Chào mừng bạn quay lại', 'Welcome back')}
        </h2>
        <form
          className="signin-form"
          onSubmit={(event) => {
            event.preventDefault();
            setBusy(true);
            setError('');
            (creating ? register : login)(form.email.trim(), form.password)
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
              autoFocus
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>
          <label htmlFor="signin-password">{bi('Mật khẩu', 'Password')}</label>
          <div className="signin-password">
            <input
              id="signin-password"
              type={reveal ? 'text' : 'password'}
              required
              minLength={creating ? 8 : undefined}
              autoComplete={creating ? 'new-password' : 'current-password'}
              aria-describedby={creating ? 'password-rules' : undefined}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
            <button
              type="button"
              aria-pressed={reveal}
              aria-label={bi('Hiện mật khẩu', 'Show password')}
              onClick={() => setReveal((shown) => !shown)}
            >
              <SkillIcon skill={reveal ? 'eyeOff' : 'eye'} />
            </button>
          </div>
          {creating && (
            <ul className="signin-rules" id="password-rules">
              {passwordRules.map((rule) => {
                const met = rule.test(form.password);
                return (
                  <li key={rule.en} className={met ? 'met' : undefined}>
                    <span aria-hidden="true">{met && <SkillIcon skill="check" size={14} />}</span>
                    {bi(rule.vi, rule.en)}
                    <span className="sr-only">
                      {met ? bi(': đạt', ': met') : bi(': chưa đạt', ': not met')}
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
          {error && <Notice error>{messages[error]}</Notice>}
          <button className="primary" disabled={busy}>
            {busy
              ? bi('Đang gửi…', 'Sending…')
              : creating
                ? bi('Tạo tài khoản', 'Create account')
                : bi('Đăng nhập', 'Sign in')}
          </button>
        </form>
        <p className="signin-note">
          {bi(
            'Email chỉ dùng để đăng nhập. Bảng xếp hạng chỉ hiện tên hiển thị bạn chọn.',
            'Your email is only for signing in. The leaderboard shows only the display name you choose.',
          )}
        </p>
        <Link className="signin-back" to={next}>
          {bi('Học tiếp không cần tài khoản', 'Keep practising without an account')}
          <SkillIcon skill="arrow" size={18} />
        </Link>
      </section>
    </div>
  );
}
