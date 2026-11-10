import { useEffect, useState } from 'react';
import { useInRouterContext, useLocation } from 'react-router-dom';
import SkillIcon, { isIconName, type IconName } from './SkillIcon';
import { liveQuery } from 'dexie';
import { useApp } from '../app/store';
import { useT, topics, topicVi } from '../i18n';
import { levelSchema, type Level } from '../data/schema';
export function useLive<T>(query: () => Promise<T>, deps: unknown[] = []) {
  const [value, setValue] = useState<T>();
  const [error, setError] = useState('');
  useEffect(() => {
    const sub = liveQuery(query).subscribe({
      next: setValue,
      error: () => setError('Không thể đọc dữ liệu / Cannot read data'),
    });
    return () => sub.unsubscribe(); // query is intentionally driven by explicit dependencies
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return { value, error };
}
export function Filters({
  availableTopics = topics,
  topicOptionGroups,
}: {
  availableTopics?: string[];
  topicOptionGroups?: { label: string; topics: readonly string[] }[];
}) {
  const t = useT();
  const { level, topic, filter, settings } = useApp();
  const choices = [...new Set([...availableTopics, ...(topic === 'all' ? [] : [topic])])];
  const options = (entries: readonly string[]) =>
    entries.map((name) => (
      <option key={name} value={name}>
        {settings.language === 'vi' ? (topicVi[name] ?? name) : name}
      </option>
    ));
  return (
    <div className="filters">
      <label>
        {t('level')}
        <select value={level} onChange={(e) => filter(e.target.value as Level | 'all', topic)}>
          <option value="all">{t('allLevels')}</option>
          {levelSchema.options.map((x) => (
            <option key={x}>{x}</option>
          ))}
        </select>
      </label>
      <label>
        {t('topic')}
        <select value={topic} onChange={(e) => filter(level, e.target.value)}>
          <option value="all">{t('allTopics')}</option>
          {topicOptionGroups
            ? topicOptionGroups.map((group) => (
                <optgroup label={group.label} key={group.label}>
                  {options(group.topics.filter((name) => choices.includes(name)))}
                </optgroup>
              ))
            : options(choices)}
        </select>
      </label>
    </div>
  );
}
export function useFiltered<T extends { level: string; topic: string }>(items: T[]) {
  const { level, topic } = useApp();
  return items.filter(
    (x) => (level === 'all' || x.level === level) && (topic === 'all' || x.topic === topic),
  );
}
export function PageTitle({
  title,
  meta,
  description,
  children,
}: {
  title: string;
  /** Facts about the item, such as level and topic, shown under the heading. */
  meta?: string;
  description?: string;
  children?: React.ReactNode;
}) {
  return (
    <header className="page-title">
      {useInRouterContext() && <PageTile />}
      <div>
        <h1>{title}</h1>
        {meta && <p className="page-meta">{meta}</p>}
        {description && <p className="muted">{description}</p>}
      </div>
      {children}
    </header>
  );
}
/** The page's pictogram on its skill-line plate, from the first part of the address. */
function PageTile() {
  const { pathname } = useLocation();
  const segment = pathname.split('/')[1] || 'dashboard';
  const icon: IconName | null =
    segment === 'account' ? 'user' : isIconName(segment) ? segment : null;
  return icon ? (
    <span className="line-tile page-tile" aria-hidden="true">
      <SkillIcon skill={icon} size={26} />
    </span>
  ) : null;
}

/** A lesson's level, on the CEFR colour scale, and its topic in the interface language. */
export function LevelTopic({
  level,
  topic,
  extra,
}: {
  level: string;
  topic: string;
  /** One more fact, such as a writing genre. */
  extra?: string;
}) {
  const language = useApp((s) => s.settings.language);
  return (
    <span className="level-topic">
      <span className="level-chip" data-level={level}>
        {level}
      </span>
      <span className="topic-chip">{language === 'vi' ? (topicVi[topic] ?? topic) : topic}</span>
      {extra && <span className="topic-chip">{extra}</span>}
    </span>
  );
}

export function Empty() {
  const t = useT();
  const filter = useApp((s) => s.filter);
  return (
    <div className="panel empty">
      <span aria-hidden="true">◇</span>
      <p>{t('empty')}</p>
      <button onClick={() => filter('all', 'all')}>{t('clearFilters')}</button>
    </div>
  );
}
export function Notice({
  children,
  error = false,
}: {
  children: React.ReactNode;
  error?: boolean;
}) {
  return (
    <p role={error ? 'alert' : 'status'} className={error ? 'notice error' : 'notice'}>
      {children}
    </p>
  );
}
export function useTimer(active = true) {
  const [start] = useState(Date.now);
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setSeconds(Math.floor((Date.now() - start) / 1000)), 1000);
    return () => clearInterval(id);
  }, [active, start]);
  return { start, seconds };
}
