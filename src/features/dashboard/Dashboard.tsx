import { Link } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import { Notice, useLive } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { db } from '../../services/storage';
import { dueQueue } from '../../services/srs';
import { getProgress, skills } from '../../services/progress';
import { recommend, type Reason } from '../../services/recommend';
import type { Skill } from '../../data/schema';
import {
  vocabulary,
  listenings,
  dictations,
  readings,
  speakingPrompts,
  writingPrompts,
  structures,
} from '../../data/content';

/** Home as a route map: today's stops first, then every skill line, then the week. */
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
  const queue = dueQueue([...vocabulary, ...custom], reviews);
  const reviewed = new Set(reviews.map((r) => r.id));
  const dueCards = queue.filter((w) => reviewed.has(w.id)).length;
  const plan = recommend(attempts, dueCards);
  const next = plan.find((step) => !progress.todaySkills.has(step.skill));
  const minutes = Math.floor(progress.todaySeconds / 60);
  const percent = Math.min(
    100,
    Math.round((progress.todaySeconds / (settings.dailyGoal * 60)) * 100),
  );
  const weekMax = Math.max(60, ...progress.week.map((w) => w.seconds));
  const weekMinutes = Math.round(progress.week.reduce((sum, w) => sum + w.seconds, 0) / 60);
  const date = new Date().toLocaleDateString(settings.language === 'vi' ? 'vi-VN' : 'en-US', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });

  const why = (reason: Reason) => {
    switch (reason.kind) {
      case 'due':
        return bi(
          `${reason.cards} thẻ đã đến hạn ôn`,
          `${reason.cards} ${reason.cards === 1 ? 'card' : 'cards'} due for review`,
        );
      case 'new':
        return bi('Bạn chưa thử kỹ năng này', 'You have not tried this skill yet');
      case 'weak':
        return bi(
          `Điểm gần đây ${reason.average}% — luyện thêm sẽ tiến bộ`,
          `Recent score ${reason.average}% — more practice will help`,
        );
      case 'stale':
        return bi(`${reason.days} ngày chưa luyện`, `Not practised for ${reason.days} days`);
      case 'keep':
        return bi(`Giữ phong độ ${reason.average}%`, `Keep up your ${reason.average}%`);
    }
  };

  const lineFacts: Record<Skill, string> = {
    vocabulary: bi(
      `${vocabulary.length} từ${dueCards ? ` · ${dueCards} thẻ đến hạn` : ''}`,
      `${vocabulary.length} words${dueCards ? ` · ${dueCards} due` : ''}`,
    ),
    listening: bi(
      `${listenings.length} bài nghe · ${dictations.length} câu chép`,
      `${listenings.length} lessons · ${dictations.length} dictations`,
    ),
    speaking: bi(`${speakingPrompts.length} đề`, `${speakingPrompts.length} prompts`),
    reading: bi(`${readings.length} bài đọc`, `${readings.length} passages`),
    writing: bi(`${writingPrompts.length} đề viết`, `${writingPrompts.length} prompts`),
    grammar: bi(`${structures.length} cấu trúc`, `${structures.length} patterns`),
  };

  return (
    <div className="home">
      <header className="home-head">
        <img
          className="home-calendar"
          src="/art/dash-calendar.webp"
          width={192}
          height={172}
          alt=""
          draggable={false}
        />
        <div>
          <h1>{bi('Hôm nay', 'Today')}</h1>
          <p className="home-date">{date}</p>
        </div>
        <svg className="home-plane" viewBox="0 0 120 40" aria-hidden="true">
          <path className="trail" d="M2 36c20-2 40-10 62-16" />
          <path className="plane" d="M118 2L74 18l14 4 4 14 8-12z" />
        </svg>
        <div className="home-signs">
          <p className="sign-plate">
            <SkillIcon skill="streak" size={18} />
            <span>
              <strong>{progress.streak}</strong> {bi('ngày liên tiếp', 'day streak')}
            </span>
          </p>
          <p className="sign-plate">
            <SkillIcon skill="goal" size={18} />
            <span>
              <strong>{minutes}</strong>/{settings.dailyGoal} {t('minutes')}
            </span>
            <progress value={percent} max={100} aria-label={t('daily')} />
          </p>
        </div>
      </header>

      <section className="panel route" aria-labelledby="route-title">
        <h2 id="route-title">
          <SkillIcon skill="chart" size={24} />
          {t('dailyPlan')}
        </h2>
        <div className="home-cheer" aria-hidden="true">
          <p>{bi('Cố lên bạn nhé!', 'You can do it!')}</p>
          <img src="/art/dash-kid.webp" width={182} height={218} alt="" draggable={false} />
        </div>
        <ol className="route-stops">
          {plan.map((step) => {
            const done = progress.todaySkills.has(step.skill);
            const current = step === next;
            return (
              <li
                key={step.skill}
                data-skill={step.skill}
                className={done ? 'route-stop done' : current ? 'route-stop next' : 'route-stop'}
              >
                <span className="route-dot" aria-hidden="true">
                  {done && <SkillIcon skill="check" size={14} />}
                </span>
                <Link to={`/${step.skill}`} aria-current={current ? 'step' : undefined}>
                  <span className="line-tile" aria-hidden="true">
                    <SkillIcon skill={step.skill} />
                  </span>
                  <span className="route-text">
                    <strong>{t(step.skill)}</strong>
                    <small>
                      {done ? bi('Đã xong hôm nay', 'Done today') : why(step.reason)} ·{' '}
                      {step.minutes} {t('minutes')}
                    </small>
                  </span>
                  {(done || current) && (
                    <span className="route-mark" aria-hidden="true">
                      <SkillIcon skill={done ? 'check' : 'arrow'} size={16} />
                    </span>
                  )}
                </Link>
              </li>
            );
          })}
        </ol>
        <div className="route-foot">
          {next ? (
            <Link className="button primary" to={`/${next.skill}`}>
              <SkillIcon skill="play" size={18} />
              {bi('Bắt đầu', 'Start')}: {t(next.skill)}
              <SkillIcon skill="arrow" size={18} />
            </Link>
          ) : (
            <p className="route-done">
              <SkillIcon skill="check" size={18} />
              {bi('Xong kế hoạch hôm nay', 'Today’s plan is done')}
            </p>
          )}
        </div>
      </section>

      <div className="home-grid">
        <section className="panel" aria-labelledby="lines-title">
          <h2 id="lines-title">
            <SkillIcon skill="achievements" size={24} />
            {bi('Kỹ năng', 'Skills')}
          </h2>
          <ul className="line-list">
            {skills.map((skill) => {
              const stats = progress.perSkill.find((p) => p.skill === skill)!;
              return (
                <li key={skill} data-skill={skill}>
                  <Link to={`/${skill}`}>
                    <span className="line-tile" aria-hidden="true">
                      <SkillIcon skill={skill} />
                    </span>
                    <span className="line-name">
                      <strong>{t(skill)}</strong>
                      <small>{lineFacts[skill]}</small>
                      {stats.count > 0 && (
                        <span className="line-meter" aria-hidden="true">
                          <i style={{ width: `${stats.average}%` }} />
                        </span>
                      )}
                    </span>
                    <span className="line-score">
                      {stats.count ? (
                        <>
                          <strong>{stats.average}%</strong>
                          <small>{bi(`${stats.count} lượt`, `${stats.count} tries`)}</small>
                        </>
                      ) : (
                        <small>{bi('Chưa luyện', 'Not started')}</small>
                      )}
                    </span>
                    <SkillIcon skill="chevron" size={18} />
                  </Link>
                </li>
              );
            })}
          </ul>
          <p className="home-note">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M9 18h6 M10 21h4 M12 3a6 6 0 0 0-3.5 10.9c.6.4 1 1.1 1 1.8V16h5v-.3c0-.7.4-1.4 1-1.8A6 6 0 0 0 12 3z" />
            </svg>
            {bi(
              'Điểm là kết quả luyện tập, không phải đánh giá trình độ.',
              'Scores reflect practice, not proficiency.',
            )}
          </p>
        </section>

        <div className="home-side">
          <section className="panel" aria-labelledby="week-title">
            <div className="panel-head">
              <h2 id="week-title">
                <SkillIcon skill="calendar" size={22} />
                {bi('Tuần này', 'This week')}
              </h2>
              <span className="muted">
                {weekMinutes} {t('minutes')}
              </span>
            </div>
            <div
              className="week-bars"
              role="img"
              aria-label={progress.week
                .map(
                  (w) =>
                    `${new Date(w.time).toLocaleDateString(settings.language)}: ${Math.round(w.seconds / 60)} ${t('minutes')}`,
                )
                .join(', ')}
            >
              {progress.week.map((w, i) => (
                <div key={w.key} className={i === 6 ? 'today' : undefined}>
                  <span>
                    <i style={{ height: `${Math.max(6, (w.seconds / weekMax) * 100)}%` }} />
                  </span>
                  <small>
                    {new Date(w.time).toLocaleDateString(settings.language, { weekday: 'narrow' })}
                  </small>
                </div>
              ))}
            </div>
          </section>

          <section className="panel" aria-labelledby="recent-title">
            <h2 id="recent-title">
              <SkillIcon skill="star" size={22} />
              {t('recent')}
            </h2>
            {attempts.length ? (
              <ul className="recent-list">
                {attempts.slice(0, 5).map((a) => (
                  <li key={a.id} data-skill={a.skill}>
                    <span className="line-tile small" aria-hidden="true">
                      <SkillIcon skill={a.skill} size={16} />
                    </span>
                    <span className="recent-text">
                      <strong>{a.label}</strong>
                      <small>
                        {new Date(a.timestamp).toLocaleString(settings.language, {
                          dateStyle: 'short',
                          timeStyle: 'short',
                        })}
                      </small>
                    </span>
                    <span className="badge">{Math.round(a.score)}%</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted">{t('noActivity')}</p>
            )}
            {error && <Notice error>{error}</Notice>}
          </section>
        </div>
      </div>
      <div className="home-foot" aria-hidden="true">
        <img src="/art/dash-books.webp" width={310} height={146} alt="" draggable={false} />
        <p>
          <span>{bi('Học mỗi ngày', 'Learn every day,')}</span>
          <span>{bi('vững tương lai', 'build your future')}</span>
        </p>
      </div>
    </div>
  );
}
