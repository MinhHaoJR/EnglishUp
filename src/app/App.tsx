import { lazy, Suspense, useEffect } from 'react';
import {
  NavLink,
  Outlet,
  createBrowserRouter,
  RouterProvider,
  useLocation,
  Link,
} from 'react-router-dom';
import { useApp } from './store';
import { useT } from '../i18n';
const Dashboard = lazy(() => import('../features/dashboard/Dashboard'));
import LanguagePicker from '../features/languages/LanguagePicker';
import SkillIcon from '../components/SkillIcon';
const LanguageWorkspace = lazy(() => import('../features/languages/LanguageWorkspace'));
import { skillSchema } from '../data/schema';
const Settings = lazy(() => import('../features/settings/Settings'));
const Vocabulary = lazy(() => import('../features/vocabulary/Vocabulary'));
const Reading = lazy(() => import('../features/reading/Reading'));
const Listening = lazy(() => import('../features/listening/Listening'));
const Speaking = lazy(() => import('../features/speaking/Speaking'));
const Writing = lazy(() => import('../features/writing/Writing'));
const Account = lazy(() => import('../features/account/Account'));
const Achievements = lazy(() => import('../features/achievements/Achievements'));
const Game = lazy(() => import('../features/game/Game'));
const Assistant = lazy(() => import('../features/assistant/Assistant'));
const Grammar = lazy(() => import('../features/grammar/Grammar'));
import ChatWidget from '../features/assistant/ChatWidget';
import { OfflineSign } from '../components/OfflineSign';
import { restoreSession, useAuth } from '../services/auth';
import { startAutoSync, syncNow, useSync } from '../services/sync';
export const APP_NAME = 'EnglishUp';
/** Home, then the six skill lines, then the services, like the groups on a station directory. */
const navGroups = [
  [['/', 'dashboard']],
  [
    ['/vocabulary', 'vocabulary'],
    ['/listening', 'listening'],
    ['/speaking', 'speaking'],
    ['/reading', 'reading'],
    ['/writing', 'writing'],
    ['/grammar', 'grammar'],
  ],
  [
    ['/assistant', 'assistant'],
    ['/game', 'game'],
    ['/achievements', 'achievements'],
    ['/settings', 'settings'],
  ],
] as const;
export function Layout() {
  const t = useT();
  const { settings, load, ready, error } = useApp();
  const { pathname } = useLocation();
  // Sentence patterns are English-only, so they never open the Japanese/Chinese workspace.
  const selectedSkill = skillSchema.exclude(['grammar']).safeParse(pathname.split('/')[1]);
  const email = useAuth((state) => state.email);
  useEffect(() => {
    void (async () => {
      await restoreSession();
      if (useAuth.getState().email) await syncNow();
    })();
    const stopAutoSync = startAutoSync();
    // A sync may bring newer settings from another device.
    const stopReload = useSync.subscribe((state, previous) => {
      if (state.lastSynced !== previous.lastSynced) void useApp.getState().load();
    });
    return () => {
      stopAutoSync();
      stopReload();
    };
  }, []);
  useEffect(() => {
    document.getElementById('main')?.focus();
    window.scrollTo(0, 0);
  }, [pathname]);
  useEffect(() => {
    void load();
  }, [load]);
  useEffect(() => {
    document.documentElement.lang = settings.language;
    document.documentElement.classList.toggle('dark', settings.theme === 'dark');
  }, [settings]);
  return (
    <>
      <a className="skip" href="#main">
        Skip to content / Đến nội dung
      </a>
      <aside className="sidebar">
        <NavLink className="brand" to="/">
          <span className="brand-mark" aria-hidden="true">
            e<span>↗</span>
          </span>
          {APP_NAME}
        </NavLink>
        {ready && <LanguagePicker />}
        <nav aria-label={t('practice')}>
          {navGroups.map((group) => (
            <div className="nav-group" key={group[0][0]}>
              {group.map(([path, label]) => (
                <NavLink key={path} to={path} end={path === '/'} data-skill={label}>
                  <span className="nav-tile" aria-hidden="true">
                    <SkillIcon skill={label} />
                  </span>
                  {t(label)}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>
      </aside>
      <div className="workspace" data-skill={pathname.split('/')[1] || 'dashboard'}>
        <div className="topbar">
          <OfflineSign />
          <Link
            className="avatar"
            to="/account"
            aria-label={
              email ??
              (settings.language === 'vi' ? 'Đăng nhập hoặc đăng ký' : 'Sign in or create account')
            }
            title={email ?? undefined}
          >
            {email ? email[0].toUpperCase() : 'U'}
          </Link>
        </div>
        <main id="main" tabIndex={-1}>
          {!ready ? (
            <p>{t('loading')}</p>
          ) : error ? (
            <p role="alert">{error}</p>
          ) : (
            <Suspense fallback={<p role="status">{t('loading')}</p>}>
              {settings.learningLanguage !== 'en' && (pathname === '/' || selectedSkill.success) ? (
                <LanguageWorkspace
                  key={`${settings.learningLanguage}-${pathname}`}
                  skill={selectedSkill.success ? selectedSkill.data : undefined}
                />
              ) : (
                <Outlet key={settings.learningLanguage} />
              )}
            </Suspense>
          )}
        </main>
      </div>
      {ready && <ChatWidget />}
    </>
  );
}
const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'vocabulary', element: <Vocabulary /> },
      { path: 'reading', element: <Reading /> },
      { path: 'listening', element: <Listening /> },
      { path: 'speaking', element: <Speaking /> },
      { path: 'writing', element: <Writing /> },
      { path: 'grammar', element: <Grammar /> },
      { path: 'settings', element: <Settings /> },
      { path: 'account', element: <Account /> },
      { path: 'assistant', element: <Assistant /> },
      { path: 'game', element: <Game /> },
      { path: 'achievements', element: <Achievements /> },
      { path: '*', element: <NotFound /> },
    ],
  },
]);
function NotFound() {
  const t = useT();
  return (
    <section className="panel">
      <h1>404</h1>
      <p>Trang không tồn tại / Page not found</p>
      <Link className="button" to="/">
        {t('dashboard')}
      </Link>
    </section>
  );
}
export default function App() {
  return <RouterProvider router={router} />;
}
