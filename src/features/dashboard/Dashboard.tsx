import { Link } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import { Filters, Notice, PageTitle, useLive } from '../../components/shared';
import { db } from '../../services/storage';
import { dueQueue } from '../../services/srs';
import { getProgress } from '../../services/progress';
import {
  vocabulary,
  listenings,
  dictations,
  readings,
  speakingPrompts,
  writingPrompts,
} from '../../data/content';
import '../../styles/vibrant-dashboard.css';
const icons = { vocabulary: 'Aa', listening: '♫', speaking: '✦', reading: '▤', writing: '✎' };
export default function Dashboard() {
  const t = useT();
  const bi = useBi();
  const { settings } = useApp();
  const { value: attempts = [], error } = useLive(() =>
    db.attempts
      .orderBy('timestamp')
      .reverse()
      .filter((a) => (a.learningLanguage ?? 'en') === 'en')
      .toArray(),
  );
  const { value: reviews = [] } = useLive(() => db.reviews.toArray());
  const { value: custom = [] } = useLive(() => db.words.toArray());
  const progress = getProgress(attempts);
  const due = dueQueue([...vocabulary, ...custom], reviews).length;
  const minutes = Math.floor(progress.todaySeconds / 60);
  const percent = Math.min(
    100,
    Math.round((progress.todaySeconds / (settings.dailyGoal * 60)) * 100),
  );
  const maxSeconds = Math.max(60, ...progress.week.map((w) => w.seconds));
  const date = new Date().toLocaleDateString(settings.language === 'vi' ? 'vi-VN' : 'en-US', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });
  const cards = [
    {
      skill: 'listening' as const,
      vi: 'Lắng nghe thế giới',
      en: 'Tune in to the world',
      descVi: 'Hội thoại đời thường & chép chính tả',
      descEn: 'Everyday conversations & dictation',
      meta: bi(
        `${listenings.length} bài nghe · ${dictations.length} câu chép`,
        `${listenings.length} lessons · ${dictations.length} dictations`,
      ),
      cls: 'peach',
    },
    {
      skill: 'speaking' as const,
      vi: 'Tự tin cất lời',
      en: 'Find your own voice',
      descVi: 'Đọc theo mẫu & nói theo chủ đề',
      descEn: 'Read aloud & explore a topic',
      meta: bi(
        `${speakingPrompts.length} đề luyện nói`,
        `${speakingPrompts.length} speaking prompts`,
      ),
      cls: 'rose',
    },
    {
      skill: 'reading' as const,
      vi: 'Mở thêm góc nhìn',
      en: 'Open a new perspective',
      descVi: 'Bài đọc ngắn, ý tưởng đáng nhớ',
      descEn: 'Short reads, memorable ideas',
      meta: bi(`${readings.length} bài đọc`, `${readings.length} stories`),
      cls: 'blue',
    },
    {
      skill: 'writing' as const,
      vi: 'Viết nên ý tưởng',
      en: 'Put ideas into words',
      descVi: 'Viết, nhận xét & tiến bộ từng bản nháp',
      descEn: 'Write, reflect & improve each draft',
      meta: bi(
        `${writingPrompts.length} đề · Nhận xét offline`,
        `${writingPrompts.length} prompts · Offline feedback`,
      ),
      cls: 'mint',
    },
  ];
  return (
    <div className="joy-dashboard">
      <PageTitle
        eyebrow={t('homeEyebrow')}
        title={bi('Hôm nay, học điều mới!', 'A new day. A new discovery!')}
        description={date}
      />
      <section className="hero">
        <div className="hero-copy">
          <span className="hero-chip">
            ✦{' '}
            {bi('MỘT CHÚT MỖI NGÀY. TIẾN XA MỖI TUẦN.', 'A LITTLE EVERY DAY. FURTHER EVERY WEEK.')}
          </span>
          <h2>
            {bi('Mở lời hôm nay.', 'Say hello today.')}
            <br />
            <em>{bi('Mở cả thế giới.', 'Open up your world.')}</em>
          </h2>
          <p>
            {bi(
              'Từ một từ mới đến một câu chuyện hay. Dành 5–10 phút khám phá tiếng Anh theo cách của bạn.',
              'From a new word to a great story. Take 5–10 minutes to explore English your way.',
            )}
          </p>
          <Link className="button primary" to={due ? '/vocabulary' : '/reading'}>
            {t('continue')} <span aria-hidden="true">→</span>
          </Link>
          <span className="hero-foot">
            {bi('Không áp lực. Chỉ cần đều đặn.', 'No pressure. Just a little consistency.')}
          </span>
        </div>
        <div className="joy-hero-art" aria-hidden="true">
          <div className="joy-art-orbit" />
          <div className="joy-art-spark">✳</div>
          <div className="joy-word-card">
            <span>ONE WORD, A NEW WORLD</span>
            <strong>
              Hello<span>.</span>
            </strong>
            <div>
              <i /> <i /> <i /> <span>↗</span>
            </div>
          </div>
          <div className="joy-speech-sticker">You got this!</div>
          <div className="joy-audio-sticker">
            <i />
            <i />
            <i />
            <i />
            <i />
            <i />
            <i />
          </div>
          <div className="joy-art-star">✦</div>
          <div className="joy-art-note">A little better, every day.</div>
        </div>
      </section>
      <div className="stats dashboard-stats">
        <div className="stat">
          <div className="stat-label">
            <span>{t('streak')}</span>
            <span aria-hidden="true">☀</span>
          </div>
          <strong>
            {progress.streak}
            <small>{bi('ngày', 'days')}</small>
          </strong>
          <span>
            {progress.streak
              ? bi('Giữ nhịp học của bạn nhé', 'Keep your rhythm going')
              : bi('Bắt đầu chuỗi ngày đầu tiên', 'Start your first streak')}
          </span>
        </div>
        <div className="stat">
          <div className="stat-label">
            <span>{t('daily')}</span>
            <span aria-hidden="true">◷</span>
          </div>
          <strong>
            {minutes}
            <small>
              / {settings.dailyGoal} {t('minutes')}
            </small>
          </strong>
          <progress value={percent} max={100} aria-label={t('daily')} />
        </div>
        <div className="stat">
          <div className="stat-label">
            <span>{t('due')}</span>
            <span aria-hidden="true">▧</span>
          </div>
          <strong>
            {due}
            <small>{bi('thẻ', 'cards')}</small>
          </strong>
          <Link className="text-link" to="/vocabulary">
            {t('review')} →
          </Link>
        </div>
        <div className="stat">
          <div className="stat-label">
            <span>{bi('Lượt luyện tập', 'Practice attempts')}</span>
            <span aria-hidden="true">↗</span>
          </div>
          <strong>
            {attempts.length}
            <small>{bi('đã hoàn thành', 'completed')}</small>
          </strong>
          <span>{bi('Mỗi lần luyện đều có giá trị', 'Every practice counts')}</span>
        </div>
      </div>
      <div className="dashboard-columns">
        <div>
          <div className="section-heading">
            <div>
              <p className="eyebrow">{bi('HỌC THEO CÁCH CỦA BẠN', 'YOUR OWN WAY TO LEARN')}</p>
              <h2>{t('choose')}</h2>
            </div>
            <span className="muted">4 {bi('kỹ năng', 'skills')}</span>
          </div>
          <Filters />
          <div className="skill-grid">
            {cards.map((c) => (
              <Link to={`/${c.skill}`} className={`skill-card ${c.cls}`} key={c.skill}>
                <div className="skill-card-top">
                  <span className="skill-icon" aria-hidden="true">
                    {icons[c.skill]}
                  </span>
                  <span className="skill-arrow">↗</span>
                </div>
                <span className="skill-label">{t(c.skill)}</span>
                <h3>{bi(c.vi, c.en)}</h3>
                <p>{bi(c.descVi, c.descEn)}</p>
                <div className="skill-meta">{c.meta}</div>
              </Link>
            ))}
          </div>
          <Link className="vocab-banner" to="/vocabulary">
            <span className="vocab-icon">Aa</span>
            <div>
              <h3>{bi('Gom từng từ, mở rộng thế giới.', 'A bigger world, one word at a time.')}</h3>
              <p>
                {bi(
                  `${vocabulary.length} từ vựng · ${new Set(vocabulary.map((word) => word.topic)).size} chủ đề · Ôn tập thông minh`,
                  `${vocabulary.length} words · ${new Set(vocabulary.map((word) => word.topic)).size} topics · Spaced repetition`,
                )}
              </p>
            </div>
            <span>→</span>
          </Link>
        </div>
        <aside className="dashboard-aside">
          <section className="panel plan-panel">
            <div className="section-heading">
              <h2>{t('dailyPlan')}</h2>
              <span className="badge">{percent}%</span>
            </div>
            <p className="muted">
              {percent >= 100
                ? bi('Bạn đã đạt mục tiêu hôm nay!', 'You reached today’s goal!')
                : bi('Dành một khoảng nhỏ cho bản thân.', 'Make a little time for yourself.')}
            </p>
            <div className="plan-list">
              {(
                [
                  {
                    skill: 'vocabulary',
                    minutes: 3,
                    vi: 'Ôn vài từ quen thuộc',
                    en: 'Revisit a few words',
                  },
                  {
                    skill: 'listening',
                    minutes: 4,
                    vi: 'Lắng nghe một hội thoại',
                    en: 'Listen to a conversation',
                  },
                  {
                    skill: 'reading',
                    minutes: 3,
                    vi: 'Khám phá một câu chuyện',
                    en: 'Explore a short story',
                  },
                ] as const
              ).map((step, i) => (
                <Link key={step.skill} to={`/${step.skill}`}>
                  <span
                    className={`plan-number ${progress.todaySkills.has(step.skill) ? 'complete' : ''}`}
                  >
                    {progress.todaySkills.has(step.skill) ? '✓' : i + 1}
                  </span>
                  <div>
                    <strong>{bi(step.vi, step.en)}</strong>
                    <small>
                      {step.minutes} {t('minutes')}
                    </small>
                  </div>
                  <span className="muted">›</span>
                </Link>
              ))}
            </div>
            <p className="plan-caption">
              {bi(
                'Gợi ý 10 phút · Tùy chọn bài bạn thích',
                'A 10-minute suggestion · Choose what you enjoy',
              )}
            </p>
          </section>
          <section className="panel week-panel">
            <h2>{bi('Nhịp học tuần này', 'Your weekly rhythm')}</h2>
            <div
              className="week-chart"
              role="img"
              aria-label={progress.week
                .map(
                  (w) =>
                    `${new Date(w.time).toLocaleDateString(settings.language)}: ${Math.round(w.seconds / 60)} ${t('minutes')}`,
                )
                .join(', ')}
            >
              {progress.week.map((w, i) => (
                <div key={w.key}>
                  <span className="bar-slot">
                    <i
                      className={i === 6 ? 'bar-today' : ''}
                      style={{
                        height: `${Math.max(4, (w.seconds / maxSeconds) * 85)}px`,
                        opacity: w.seconds ? 1 : 0.2,
                      }}
                    />
                  </span>
                  <small>
                    {new Date(w.time).toLocaleDateString(settings.language, { weekday: 'narrow' })}
                  </small>
                </div>
              ))}
            </div>
            <p className="muted">
              {bi('Từng phút nhỏ tạo nên thay đổi.', 'Small minutes add up to change.')}
            </p>
          </section>
          <div className="quote-card">
            <span aria-hidden="true">“</span>
            <p>
              You don’t have to be great
              <br />
              to get started.
            </p>
            <small>
              {bi('Cứ bắt đầu. Bạn sẽ tiến bộ.', 'Start where you are. Grow as you go.')}
            </small>
          </div>
        </aside>
      </div>
      <section className="panel mt-7">
        <h2>{t('progress')}</h2>
        <div className="progress-grid">
          {progress.perSkill.map((p) => (
            <div key={p.skill}>
              <div className="flex justify-between mb-2">
                <strong>{t(p.skill)}</strong>
                <span className="muted">{p.count ? `${p.average}%` : '—'}</span>
              </div>
              <progress max={100} value={p.average} aria-label={t(p.skill)} />
              <p className="muted mt-2">
                {p.count} {bi('lượt · điểm trung bình', 'attempts · average score')}
              </p>
            </div>
          ))}
        </div>
        <p className="muted mt-4">
          {bi(
            'Điểm là kết quả luyện tập, không phải đánh giá trình độ. Luyện nói có thể là tự đánh giá; luyện viết dùng quy tắc offline.',
            'Scores reflect practice, not proficiency. Speaking can be self-assessed; writing uses offline rules.',
          )}
        </p>
      </section>
      <section className="panel">
        <h2>{t('recent')}</h2>
        {attempts.length ? (
          <div className="activity-list">
            {attempts.slice(0, 8).map((a) => (
              <div key={a.id}>
                <span className="activity-icon" aria-hidden="true">
                  {icons[a.skill]}
                </span>
                <div>
                  <strong>{a.label}</strong>
                  <small>
                    {t(a.skill)} · {new Date(a.timestamp).toLocaleString(settings.language)} ·{' '}
                    {a.duration}s
                  </small>
                </div>
                <span className="badge">{Math.round(a.score)}%</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted">{t('noActivity')}</p>
        )}
        {error && <Notice error>{error}</Notice>}
      </section>
    </div>
  );
}
