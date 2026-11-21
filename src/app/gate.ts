import type { Settings } from '../services/storage';

/**
 * Paths a learner may open before taking the level test: the test itself, sign-in (an account may
 * already hold a result from another device) and the admin area, which has its own entrance.
 */
const OPEN_BEFORE_TEST = ['/placement', '/login', '/admin'];

/** True until the learner has a level test result on this device or in their synced settings. */
export function needsLevelTest(settings: Pick<Settings, 'placement'>) {
  return !settings.placement;
}

/** Where the shell sends a path: the level test first, then anywhere. */
export function gateTarget(settings: Pick<Settings, 'placement'>, pathname: string) {
  return needsLevelTest(settings) && !OPEN_BEFORE_TEST.includes(pathname) ? '/placement' : null;
}
