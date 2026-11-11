import { useState } from 'react';
import { useApp } from '../app/store';
import { useBi, useT, topics as topicOrder, topicVi } from '../i18n';
import { levelSchema, type Level, type Skill } from '../data/schema';
import { db } from '../services/storage';
import { useLive, LevelTopic, Empty } from './shared';
import SkillIcon from './SkillIcon';

const PAGE = 12;
type Lesson = { id: string; title: string; level: Level; topic: string };

/** Easiest first; lessons an admin adds later are stored last, whatever their level. */
export const byLevel = <T extends { level: Level }>(items: T[]) =>
  [...items].sort(
    (a, b) => levelSchema.options.indexOf(a.level) - levelSchema.options.indexOf(b.level),
  );

/** Best saved score per lesson title. Speaking labels add "(alignment)" or "(self-assessed)". */
function useBestScores(skill: Skill) {
  const { value: attempts = [] } = useLive(
    () => db.attempts.where('skill').equals(skill).toArray(),
    [skill],
  );
  const best = new Map<string, number>();
  for (const attempt of attempts) {
    const title = attempt.label.replace(/ \((alignment|self-assessed)\)$/, '');
    best.set(title, Math.max(best.get(title) ?? 0, attempt.score));
  }
  return best;
}

/**
 * The lesson list shared by reading, listening, speaking and writing: a level band with progress,
 * topic and title search, a "next lesson" shortcut and cards that open with one click anywhere.
 * Level and topic are the app-wide filters, so links from the learning paths land on the right level.
 */
export function LessonBrowser<T extends Lesson>({
  skill,
  all,
  describe,
  onOpen,
  keyOf = (lesson) => lesson.title,
}: {
  skill: Skill;
  /** Every lesson of this list (one speaking mode, say), before the level and topic filters. */
  all: T[];
  describe: (lesson: T) => { preview?: string; meta: string; extra?: string };
  onOpen: (lesson: T) => void;
  /** The attempt label that marks a lesson done; the title unless the page logs something else. */
  keyOf?: (lesson: T) => string;
}) {
  const t = useT();
  const bi = useBi();
  const { level, topic, filter, settings } = useApp();
  const best = useBestScores(skill);
  const [query, setQuery] = useState('');
  const [todoOnly, setTodoOnly] = useState(false);
  const [paging, setPaging] = useState({ key: '', count: PAGE });

  const inTopic = all.filter((lesson) => topic === 'all' || lesson.topic === topic);
  const needle = query.trim().toLowerCase();
  const visible = inTopic.filter(
    (lesson) =>
      (level === 'all' || lesson.level === level) &&
      (!needle || lesson.title.toLowerCase().includes(needle)) &&
      (!todoOnly || !best.has(keyOf(lesson))),
  );
  const key = `${level}|${topic}|${needle}|${todoOnly}`;
  const count = paging.key === key ? paging.count : PAGE;
  const next = visible.find((lesson) => !best.has(keyOf(lesson)));
  const present = topicOrder.filter((name) => all.some((lesson) => lesson.topic === name));
  const topicName = (name: string) => (settings.language === 'vi' ? (topicVi[name] ?? name) : name);

  return (
    <div className="lesson-browser">
      <nav className="level-band" aria-label={bi('Chọn trình độ', 'Choose a level')}>
        {(['all', ...levelSchema.options] as const).map((value) => {
          const group = value === 'all' ? inTopic : inTopic.filter((l) => l.level === value);
          const done = group.filter((lesson) => best.has(keyOf(lesson))).length;
          return (
            <button
              key={value}
              type="button"
              data-level={value}
              aria-pressed={level === value}
              onClick={() => filter(value, topic)}
            >
              <strong>{value === 'all' ? bi('Tất cả', 'All') : value}</strong>
              <small>
                {done}/{group.length}{' '}
                <span className="level-done-word">{bi('đã làm', 'done')}</span>
              </small>
              <span className="level-meter" aria-hidden="true">
                <span style={{ width: `${group.length ? (done / group.length) * 100 : 0}%` }} />
              </span>
            </button>
          );
        })}
      </nav>

      <div className="lesson-tools">
        <label>
          {t('topic')}
          <select value={topic} onChange={(event) => filter(level, event.target.value)}>
            <option value="all">{t('allTopics')}</option>
            {[...present, ...(topic !== 'all' && !present.includes(topic) ? [topic] : [])].map(
              (name) => (
                <option key={name} value={name}>
                  {topicName(name)}
                </option>
              ),
            )}
          </select>
        </label>
        <label>
          {bi('Tìm bài', 'Search lessons')}
          <input
            type="search"
            value={query}
            placeholder={bi('Tên bài…', 'Lesson title…')}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
        <label className="lesson-todo">
          <input
            type="checkbox"
            checked={todoOnly}
            onChange={(event) => setTodoOnly(event.target.checked)}
          />
          {bi('Chỉ bài chưa làm', 'Not done yet')}
        </label>
        {next && (
          <button type="button" className="primary lesson-next" onClick={() => onOpen(next)}>
            <SkillIcon skill="goal" size={18} />
            <span>
              {bi('Bài tiếp theo', 'Next lesson')}: <strong>{next.title}</strong>
            </span>
          </button>
        )}
      </div>

      {visible.length ? (
        <>
          <p className="lesson-count muted" role="status">
            {bi(
              `${visible.length} bài · đang hiện ${Math.min(count, visible.length)}`,
              `${visible.length} lessons · showing ${Math.min(count, visible.length)}`,
            )}
          </p>
          <div className="lesson-grid">
            {visible.slice(0, count).map((lesson) => {
              const { preview, meta, extra } = describe(lesson);
              const score = best.get(keyOf(lesson));
              return (
                <article className="panel lesson-card" key={lesson.id}>
                  <div className="lesson-card-head">
                    <LevelTopic level={lesson.level} topic={lesson.topic} extra={extra} />
                    {score !== undefined && (
                      <span className="lesson-done">
                        <SkillIcon skill="check" size={14} />
                        {score}%
                      </span>
                    )}
                  </div>
                  <h2>{lesson.title}</h2>
                  {preview && <p className="muted lesson-preview">{preview}</p>}
                  <p className="lesson-meta">{meta}</p>
                  <button className="primary lesson-open" onClick={() => onOpen(lesson)}>
                    {score === undefined ? t('start') : bi('Làm lại', 'Try again')} →
                  </button>
                </article>
              );
            })}
          </div>
          {visible.length > count && (
            <button
              type="button"
              className="lesson-more"
              onClick={() => setPaging({ key, count: count + PAGE })}
            >
              {bi(
                `Xem thêm ${Math.min(PAGE, visible.length - count)} bài (còn ${visible.length - count})`,
                `Show ${Math.min(PAGE, visible.length - count)} more (${visible.length - count} left)`,
              )}
            </button>
          )}
        </>
      ) : (
        <Empty />
      )}
    </div>
  );
}
