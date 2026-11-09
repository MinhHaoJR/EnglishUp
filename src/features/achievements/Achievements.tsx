import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import { useAuth } from '../../services/auth';
import { useSync } from '../../services/sync';
import {
  fetchAchievements,
  fetchLeaderboard,
  type Achievement,
  type Leaderboard,
  type Period,
} from '../../services/community';

/** Bilingual names for the server's badge codes: [vi title, en title, vi description, en description]. */
const badgeText: Record<string, [string, string, string, string]> = {
  'first-practice': [
    'Bước đầu tiên',
    'First step',
    'Hoàn thành lượt luyện tập đầu tiên.',
    'Finish your first practice.',
  ],
  'streak-3': [
    'Ba ngày liền',
    'Three in a row',
    'Luyện tập 3 ngày liên tiếp.',
    'Practise 3 days in a row.',
  ],
  'streak-7': [
    'Một tuần bền bỉ',
    'Steady week',
    'Luyện tập 7 ngày liên tiếp.',
    'Practise 7 days in a row.',
  ],
  'all-skills': [
    'Đủ năm kỹ năng',
    'All five skills',
    'Luyện đủ từ vựng, nghe, nói, đọc và viết.',
    'Practise vocabulary, listening, speaking, reading and writing.',
  ],
  'perfect-10': [
    'Mười lần tuyệt đối',
    'Perfect ten',
    'Đạt 100% trong 10 lượt luyện tập.',
    'Score 100% in 10 practices.',
  ],
  'words-100': [
    'Trăm từ',
    'Hundred words',
    'Ôn tập 100 từ vựng khác nhau.',
    'Review 100 different words.',
  ],
};

export default function Achievements() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const lastSynced = useSync((state) => state.lastSynced);
  const [period, setPeriod] = useState<Period>('week');
  const [badges, setBadges] = useState<Achievement[] | null>(null);
  const [board, setBoard] = useState<Leaderboard | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (!email) return;
    let current = true;
    Promise.all([fetchAchievements(), fetchLeaderboard(period)])
      .then(([nextBadges, nextBoard]) => {
        if (!current) return;
        setBadges(nextBadges);
        setBoard(nextBoard);
        setFailed(false);
      })
      .catch(() => current && setFailed(true));
    return () => {
      current = false;
    };
  }, [email, period, lastSynced]);

  const title = <PageTitle title={bi('Thành tích', 'Achievements')} />;

  if (!email)
    return (
      <>
        {title}
        <Notice>
          {bi('Hãy', 'Please')}{' '}
          <Link to="/account">
            {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
          </Link>{' '}
          {bi(
            'để nhận điểm, huy hiệu và xem bảng xếp hạng.',
            'to earn points and badges and see the leaderboard.',
          )}
        </Notice>
      </>
    );

  return (
    <>
      {title}
      {failed && (
        <Notice error>
          {bi(
            'Không tải được thành tích. Hãy kiểm tra kết nối rồi thử lại.',
            'Could not load achievements. Check your connection and try again.',
          )}
        </Notice>
      )}
      <section className="space-y-4">
        <h2>{bi('Huy hiệu', 'Badges')}</h2>
        {!badges && !failed && <p role="status">{bi('Đang tải…', 'Loading…')}</p>}
        <ul className="lesson-grid" aria-label={bi('Huy hiệu', 'Badges')}>
          {badges?.map((badge) => {
            const [viTitle, enTitle, viText, enText] = badgeText[badge.code] ?? [
              badge.code,
              badge.code,
              '',
              '',
            ];
            return (
              <li
                key={badge.code}
                className={`panel lesson-card${badge.earnedAt ? '' : ' locked'}`}
              >
                <h3>{bi(viTitle, enTitle)}</h3>
                <p className="muted">{bi(viText, enText)}</p>
                <span className="badge">
                  {badge.earnedAt
                    ? `${bi('Đã đạt', 'Earned')} ${new Date(badge.earnedAt).toLocaleDateString()} · +${badge.points}`
                    : `${bi('Chưa đạt', 'Locked')} · +${badge.points} ${bi('điểm', 'points')}`}
                </span>
              </li>
            );
          })}
        </ul>
      </section>
      <section className="panel space-y-4">
        <h2>{bi('Bảng xếp hạng', 'Leaderboard')}</h2>
        <div className="tabs">
          {(['week', 'all'] as const).map((value) => (
            <button key={value} aria-pressed={period === value} onClick={() => setPeriod(value)}>
              {value === 'week' ? bi('Tuần này', 'This week') : bi('Mọi thời gian', 'All time')}
            </button>
          ))}
        </div>
        {board && !board.myRowShown && (
          <Notice>
            {bi(
              `Bạn có ${board.myPoints} điểm nhưng đang ẩn khỏi bảng xếp hạng. Bật hiển thị trong`,
              `You have ${board.myPoints} points but are hidden from the leaderboard. Turn it on in`,
            )}{' '}
            <Link to="/account">{bi('Tài khoản', 'Account')}</Link>.
          </Notice>
        )}
        {board &&
          (board.entries.length ? (
            <div className="activity-list" role="list">
              {board.entries.map((entry) => (
                <div key={entry.rank} role="listitem" aria-current={entry.isMe || undefined}>
                  <span className="activity-icon" aria-label={bi('Hạng', 'Rank')}>
                    {entry.rank}
                  </span>
                  <div>
                    <strong>
                      {entry.displayName}
                      {entry.isMe && ` (${bi('bạn', 'you')})`}
                    </strong>
                  </div>
                  <span className="badge">
                    {entry.points} {bi('điểm', 'points')}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">
              {bi('Chưa có ai trên bảng xếp hạng.', 'Nobody is on the leaderboard yet.')}
            </p>
          ))}
      </section>
    </>
  );
}
