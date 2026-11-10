import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useBi, useT } from '../../i18n';
import { Notice, PageTitle, useLive } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { logout, useAuth } from '../../services/auth';
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

/*
THESIS: the account as a diptych. What only you see (email, points, sync) stands permanently beside
what everyone sees (your leaderboard row, live while you edit), then your learning journey as a route.
Refuses the settings form stack with stat boxes.
OWN-WORLD: the app's wayfinding signage. The private side is a sign-blue plate, the public side a
panel with your row lit in signal yellow, the journey uses the six skill-line colours.
STORY: the learner checks points and sync, decides how they appear to others, and sees the days they studied.
FIRST VIEWPORT: two plates side by side under the title, the journey starting below.
FORM: structure #3 of 6 (timeline), "diptych comparison" composition, surface roll seed 443a6945/0.
FINISH: critique pass in light, dark and 375px, then DESIGN.md.
*/

const initial = (name: string) => (name.trim()[0] ?? '?').toUpperCase();

type Day = { time: number; skills: Set<string>; count: number; seconds: number; badges: string[] };

export default function Account() {
  const bi = useBi();
  const t = useT();
  const locale = useApp((state) => (state.settings.language === 'vi' ? 'vi-VN' : 'en-US'));
  const email = useAuth((state) => state.email);
  const { status, lastSynced, points } = useSync();
  const { value: attempts = [] } = useLive(() => db.attempts.toArray());
  const [badges, setBadges] = useState<Achievement[]>([]);
  const [rank, setRank] = useState<number | null>(null);

  useEffect(() => {
    if (!email) return;
    let current = true;
    fetchAchievements()
      .then((list) => current && setBadges(list.filter((b) => b.earnedAt)))
      .catch(() => undefined);
    fetchLeaderboard('all')
      .then((board) => current && setRank(board.entries.find((e) => e.isMe)?.rank ?? null))
      .catch(() => undefined);
    return () => {
      current = false;
    };
  }, [email, lastSynced]);

  // Signed-out learners sign in on the full-screen entrance and come back here.
  if (!email) return <Navigate to="/login?next=/account" replace />;

  const { streak } = getProgress(attempts);
  const cap = points?.dailyCap ?? 300;

  // The journey: the last active days, newest first, with badges marked on the day they were earned.
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

  return (
    <>
      <PageTitle title={bi('Tài khoản', 'Account')} />
      <div className="profile-diptych">
        <section className="profile-plate" aria-labelledby="private-title">
          <h2 id="private-title">{bi('Chỉ bạn thấy', 'Only you see')}</h2>
          <div className="profile-id">
            <span className="profile-monogram" aria-hidden="true">
              {initial(email)}
            </span>
            <strong>{email}</strong>
          </div>
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
          <div className="profile-sync">
            <p role="status">
              <SkillIcon skill="sync" size={18} />
              {status === 'syncing'
                ? bi('Đang đồng bộ…', 'Syncing…')
                : lastSynced
                  ? `${bi('Đồng bộ lần cuối', 'Last synced')}: ${new Date(lastSynced).toLocaleTimeString(locale)}`
                  : bi('Chưa đồng bộ trong phiên này.', 'Not synced in this session.')}
            </p>
            <div className="actions">
              <button disabled={status === 'syncing'} onClick={() => void syncNow()}>
                {bi('Đồng bộ ngay', 'Sync now')}
              </button>
              <button onClick={logout}>{bi('Đăng xuất', 'Sign out')}</button>
            </div>
          </div>
          {status === 'error' && (
            <Notice error>
              {bi(
                'Không đồng bộ được. Dữ liệu trên thiết bị này vẫn an toàn; hãy thử lại khi có mạng.',
                'Sync failed. Data on this device is safe; try again when you are online.',
              )}
            </Notice>
          )}
          <p className="profile-small">
            {bi(
              'Tiến độ được gộp giữa thiết bị này và tài khoản khi mở ứng dụng, sau mỗi lượt luyện tập hoặc khi bấm Đồng bộ. Xoá từ hay đặt lại dữ liệu chỉ có tác dụng trên thiết bị này.',
              'Progress merges between this device and your account when the app opens, after each practice or when you select Sync. Deleting words or resetting data only affects this device.',
            )}
          </p>
        </section>

        <ProfileForm rank={rank} total={points?.total ?? 0} />
      </div>

      <section className="journey" aria-labelledby="journey-title">
        <h2 id="journey-title">{bi('Hành trình học', 'Learning journey')}</h2>
        {journey.length ? (
          <ol>
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
        ) : (
          <p className="muted">
            {bi(
              'Chưa có buổi học nào trên thiết bị này. Hoàn thành một bài để bắt đầu hành trình.',
              'No sessions on this device yet. Finish a lesson to start your journey.',
            )}
          </p>
        )}
      </section>
    </>
  );
}

/** Display name and leaderboard opt-in, with a live preview of the row others see; never the email. */
function ProfileForm({ rank, total }: { rank: number | null; total: number }) {
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

  return (
    <section className="profile-public" aria-labelledby="public-title">
      <h2 id="public-title">{bi('Mọi người thấy', 'Everyone sees')}</h2>
      {!profile ? (
        state === 'error' ? (
          <Notice error>{bi('Không tải được hồ sơ.', 'Could not load your profile.')}</Notice>
        ) : (
          <p className="muted">{bi('Đang tải hồ sơ…', 'Loading your profile…')}</p>
        )
      ) : (
        <>
          <figure className="profile-preview">
            {profile.showOnLeaderboard ? (
              <div className="profile-row">
                <span className="profile-rank">{rank ?? '–'}</span>
                <span className="profile-monogram" aria-hidden="true">
                  {initial(profile.displayName)}
                </span>
                <strong>{profile.displayName.trim() || '…'}</strong>
                <span className="profile-points">
                  {total} {bi('điểm', 'pts')}
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
                'Xem trước hàng của bạn trên bảng xếp hạng mọi thời gian. Email không bao giờ hiện ở đây.',
                'A preview of your all-time leaderboard row. Your email never appears here.',
              )}
            </figcaption>
          </figure>
          <form
            className="profile-form"
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
        </>
      )}
    </section>
  );
}
