import { useEffect, useState } from 'react';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import { Navigate } from 'react-router-dom';
import { logout, useAuth } from '../../services/auth';
import { syncNow, useSync } from '../../services/sync';
import { fetchProfile, saveProfile, type Profile } from '../../services/community';

export default function Account() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const { status, lastSynced, points } = useSync();
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
                ? `${bi('Đồng bộ lần cuối', 'Last synced')}: ${new Date(lastSynced).toLocaleTimeString(bi('vi-VN', 'en-US'))}`
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

  // Signed-out learners sign in on the full-screen entrance and come back here.
  return <Navigate to="/login?next=/account" replace />;
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
