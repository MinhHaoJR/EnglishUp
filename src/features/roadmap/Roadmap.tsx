import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { roadmaps } from '../../data/content';
import {
  quizCategories,
  roadmapSkillLabels,
  type QuizCategory,
  type Roadmap as Path,
} from '../../data/schema';
import { roadmapFor } from '../../services/placement';

type Task = Path['stages'][number]['tasks'][number];

/** Where each kind of task opens, its pictogram and the skill line that colours it. */
const targets: Record<
  Task['skill'],
  { icon: IconName; skill: string; path: (task: Task) => string }
> = {
  vocabulary: { icon: 'vocabulary', skill: 'vocabulary', path: () => '/vocabulary' },
  translation: { icon: 'choice', skill: 'vocabulary', path: () => '/vocabulary?tab=translation' },
  relations: { icon: 'cards', skill: 'vocabulary', path: () => '/vocabulary?tab=relations' },
  grammar: { icon: 'grammar', skill: 'grammar', path: () => '/grammar' },
  reading: { icon: 'reading', skill: 'reading', path: () => '/reading' },
  listening: { icon: 'listening', skill: 'listening', path: () => '/listening' },
  speaking: { icon: 'speaking', skill: 'speaking', path: () => '/speaking' },
  writing: { icon: 'writing', skill: 'writing', path: () => '/writing' },
  wordgame: { icon: 'game', skill: 'vocabulary', path: (t) => `/game?level=${t.level}` },
  grammargame: {
    icon: 'game',
    skill: 'grammar',
    path: (t) =>
      `/game?mode=grammar&level=${t.level}${t.category ? `&category=${t.category}` : ''}`,
  },
  assistant: { icon: 'assistant', skill: 'service', path: () => '/assistant' },
  placement: { icon: 'placement', skill: 'service', path: () => '/placement' },
};

/** Learning paths from A1 to C2: pick the step you are on, then work through its stages and tasks. */
export default function Roadmap() {
  const bi = useBi();
  const navigate = useNavigate();
  const { settings, update, filter } = useApp();
  const [params, setParams] = useSearchParams();
  const followed = settings.roadmap?.id;
  // The address wins, then the path being followed, then the one the level test points to.
  const suggested = settings.placement ? roadmapFor(settings.placement.level) : undefined;
  const id = params.get('path') ?? followed ?? suggested ?? roadmaps[0]?.id;
  const path = roadmaps.find((r) => r.id === id) ?? roadmaps[0];

  const title = (
    <PageTitle
      title={bi('Lộ trình học', 'Learning paths')}
      description={bi(
        'Chọn chặng bạn đang đứng, rồi làm lần lượt từng nhiệm vụ. Mỗi nhiệm vụ mở đúng bài luyện ở đúng trình độ.',
        'Choose the step you are on, then work through each task. Every task opens the right practice at the right level.',
      )}
    />
  );
  if (!path)
    return (
      <>
        {title}
        <Notice>{bi('Chưa có lộ trình nào.', 'There are no learning paths yet.')}</Notice>
      </>
    );

  const done = new Set(settings.roadmap?.done[path.id] ?? []);
  const tasks = path.stages.flatMap((s) => s.tasks);
  const finished = tasks.filter((t) => done.has(t.id)).length;
  const share = tasks.length ? Math.round((finished / tasks.length) * 100) : 0;

  /** Ticks or unticks a task; ticking also makes this the path being followed. */
  function toggle(task: Task) {
    const next = new Set(done);
    if (next.has(task.id)) next.delete(task.id);
    else next.add(task.id);
    void update({
      roadmap: {
        id: path.id,
        done: { ...(settings.roadmap?.done ?? {}), [path.id]: [...next] },
      },
    });
  }

  function open(task: Task) {
    // The practice pages share the level filter, so the lessons match the task.
    filter(task.level, 'all');
    navigate(targets[task.skill].path(task));
  }

  return (
    <>
      {title}
      {!settings.placement && (
        <Notice>
          {bi('Chưa biết trình độ của mình?', 'Not sure of your level?')}{' '}
          <Link to="/placement">
            {bi('Làm bài kiểm tra trình độ (30 câu)', 'Take the level test (30 questions)')}
          </Link>{' '}
          {bi('để được gợi ý lộ trình phù hợp.', 'to get the right path suggested.')}
        </Notice>
      )}
      <nav className="roadmap-ladder" aria-label={bi('Các lộ trình', 'Learning paths')}>
        {roadmaps.map((r) => (
          <button
            key={r.id}
            type="button"
            aria-current={r.id === path.id ? 'step' : undefined}
            onClick={() => setParams({ path: r.id })}
          >
            <strong>
              {r.from} <SkillIcon skill="arrow" size={14} /> {r.to}
            </strong>
            <small>
              {r.id === followed
                ? bi('Đang theo', 'Following')
                : r.id === suggested
                  ? bi('Gợi ý cho bạn', 'Suggested')
                  : bi(`${r.weeks} tuần`, `${r.weeks} weeks`)}
            </small>
          </button>
        ))}
      </nav>

      <section className="panel roadmap-head" aria-labelledby="roadmap-title">
        <div>
          <h2 id="roadmap-title">{bi(path.title.vi, path.title.en)}</h2>
          <p className="muted">{bi(path.summary.vi, path.summary.en)}</p>
          <p className="roadmap-facts">
            <span>{bi(`Khoảng ${path.weeks} tuần`, `About ${path.weeks} weeks`)}</span>
            <span>{bi(`${path.stages.length} chặng`, `${path.stages.length} stages`)}</span>
            <span>{bi(`${tasks.length} nhiệm vụ`, `${tasks.length} tasks`)}</span>
          </p>
        </div>
        <div className="roadmap-progress">
          <strong>{share}%</strong>
          <span>
            {bi(
              `${finished}/${tasks.length} nhiệm vụ xong`,
              `${finished} of ${tasks.length} tasks done`,
            )}
          </span>
          <progress
            value={finished}
            max={tasks.length}
            aria-label={bi('Tiến độ lộ trình', 'Path progress')}
          />
          {followed !== path.id && (
            <button
              type="button"
              className="primary"
              onClick={() =>
                void update({
                  roadmap: { id: path.id, done: settings.roadmap?.done ?? {} },
                })
              }
            >
              {bi('Theo lộ trình này', 'Follow this path')}
            </button>
          )}
        </div>
      </section>

      <ol className="roadmap-stages">
        {path.stages.map((stage, index) => {
          const stageDone = stage.tasks.filter((t) => done.has(t.id)).length;
          const complete = stageDone === stage.tasks.length;
          return (
            <li key={stage.id} className={complete ? 'complete' : undefined}>
              <span className="roadmap-stop" aria-hidden="true">
                {complete ? <SkillIcon skill="check" size={18} /> : index + 1}
              </span>
              <section className="panel" aria-labelledby={`stage-${stage.id}`}>
                <header>
                  <h3 id={`stage-${stage.id}`}>
                    {bi(`Chặng ${index + 1}`, `Stage ${index + 1}`)}:{' '}
                    {bi(stage.title.vi, stage.title.en)}
                  </h3>
                  <span className="roadmap-count">
                    {stageDone}/{stage.tasks.length}
                  </span>
                </header>
                <p className="muted">{bi(stage.goal.vi, stage.goal.en)}</p>
                <ul className="roadmap-tasks">
                  {stage.tasks.map((task) => {
                    const target = targets[task.skill];
                    const checked = done.has(task.id);
                    return (
                      <li
                        key={task.id}
                        data-skill={target.skill}
                        className={checked ? 'done' : undefined}
                      >
                        <label className="roadmap-check">
                          <input type="checkbox" checked={checked} onChange={() => toggle(task)} />
                          <span className="sr-only">{bi('Đã xong', 'Done')}</span>
                        </label>
                        <span className="line-tile small" aria-hidden="true">
                          <SkillIcon skill={target.icon} size={16} />
                        </span>
                        <div className="roadmap-task-text">
                          <span>{bi(task.vi, task.en)}</span>
                          <small>
                            {bi(...roadmapSkillLabels[task.skill])} · {task.level}
                            {task.category &&
                              ` · ${bi(quizCategories[task.category as QuizCategory][0], quizCategories[task.category as QuizCategory][1])}`}
                          </small>
                        </div>
                        <button type="button" onClick={() => open(task)}>
                          {bi('Mở bài luyện', 'Open')}
                          <SkillIcon skill="arrow" size={16} />
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </section>
            </li>
          );
        })}
      </ol>
    </>
  );
}
