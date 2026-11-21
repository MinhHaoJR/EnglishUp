import type { IconName } from '../../components/SkillIcon';
import type { Roadmap as Path } from '../../data/schema';

export type Task = Path['stages'][number]['tasks'][number];

/** Where each kind of task opens, its pictogram and the skill line that colours it. */
export const targets: Record<
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
  tenses: { icon: 'grammar', skill: 'grammar', path: () => '/grammar?part=tenses' },
  assistant: { icon: 'assistant', skill: 'service', path: () => '/assistant' },
  placement: { icon: 'placement', skill: 'service', path: () => '/placement' },
};

/** The first task of a path that is not ticked yet, in stage order. */
export function nextTask(path: Path, done: string[]) {
  return path.stages.flatMap((s) => s.tasks).find((t) => !done.includes(t.id));
}
