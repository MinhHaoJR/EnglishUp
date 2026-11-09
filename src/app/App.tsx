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
import { languageNames } from '../data/languages';
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
import ChatWidget from '../features/assistant/ChatWidget';
import { restoreSession, useAuth } from '../services/auth';
import { startAutoSync, syncNow, useSync } from '../services/sync';
export const APP_NAME = 'EnglishUp';
export function Layout() {
  const t = useT();
  const { settings, load, ready, error } = useApp();
  const { pathname } = useLocation();
  const selectedSkill = skillSchema.safeParse(pathname.split('/')[1]);
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
          <span className="brand-mark">
            e<span>↗</span>
          </span>
          {APP_NAME}
          <span className="brand-dot">.</span>
        </NavLink>
        {ready && <LanguagePicker />}
        <p className="sidebar-caption">{t('practice')}</p>
        <nav aria-label={t('practice')}>
          {(
            [
              ['/', 'dashboard'],
              ['/vocabulary', 'vocabulary'],
              ['/listening', 'listening'],
              ['/speaking', 'speaking'],
              ['/reading', 'reading'],
              ['/writing', 'writing'],
              ['/assistant', 'assistant'],
              ['/game', 'game'],
              ['/achievements', 'achievements'],
              ['/settings', 'settings'],
            ] as const
          ).map(([path, label]) => (
            <NavLink key={path} to={path} end={path === '/'} data-skill={label}>
              <span aria-hidden="true">
                <SkillIcon skill={label} />
              </span>
              {t(label)}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-note">
          <span className="plant" aria-hidden="true">
            ✳
          </span>
          <strong>{t('tagline')}</strong>
          <p>{t('local')}</p>
        </div>
      </aside>
      <div className="workspace" data-skill={pathname.split('/')[1] || 'dashboard'}>
        <div className="topbar">
          <span>
            {languageNames[settings.learningLanguage][settings.language]} · {t('tagline')}
          </span>
          <div className="flex items-center gap-3">
            <span className="online-dot" />
            <span>
              {settings.language === 'vi' ? 'Không gian học cá nhân' : 'Personal learning space'}
            </span>
            <Link
              className="avatar"
              to="/account"
              aria-label={
                email ??
                (settings.language === 'vi'
                  ? 'Đăng nhập hoặc đăng ký'
                  : 'Sign in or create account')
              }
              title={email ?? undefined}
            >
              {email ? email[0].toUpperCase() : 'U'}
            </Link>
          </div>
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
        <footer>
          {APP_NAME} · {t('local')}
        </footer>
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
