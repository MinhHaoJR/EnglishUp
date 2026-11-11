import { useState } from 'react';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import { PageTitle, Notice } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { Flag } from '../../components/Flag';
import {
  download,
  exportData,
  importData,
  resetData,
  backupSchema,
  type Settings as SettingsType,
} from '../../services/storage';
export default function Settings() {
  const t = useT();
  const bi = useBi();
  const { settings, update, load, bump } = useApp();
  const [message, setMessage] = useState<'' | 'saved' | 'error' | 'valid' | 'invalid'>('');
  const [error, setError] = useState(false);
  const [reset, setReset] = useState(false);
  const [confirmation, setConfirmation] = useState('');
  const [pending, setPending] = useState<unknown>();
  async function run(fn: () => Promise<unknown>) {
    try {
      await fn();
      setError(false);
      setMessage('saved');
    } catch {
      setError(true);
      setMessage('error');
    }
  }
  const change = (patch: Partial<SettingsType>) => void run(() => update(patch));
  return (
    <>
      <PageTitle
        title={t('settings')}
        description={bi('Tuỳ chỉnh trải nghiệm học tập của bạn', 'Tune how you study')}
      />
      <section className="panel settings-panel">
        <div className="settings-column">
          <label className="settings-field">
            <span className="settings-label">
              <SkillIcon skill="globe" size={20} />
              {t('language')}
            </span>
            <span className="settings-control">
              <Flag code={settings.language === 'vi' ? 'vi' : 'en'} />
              <select
                value={settings.language}
                onChange={(e) => change({ language: e.target.value as 'vi' | 'en' })}
              >
                <option value="vi">Tiếng Việt</option>
                <option value="en">English</option>
              </select>
            </span>
          </label>
          <label className="settings-field">
            <span className="settings-label">
              <SkillIcon skill="gauge" size={20} />
              {t('rate')}: {settings.rate}×
            </span>
            <input
              type="range"
              className="settings-range"
              min="0.5"
              max="1.5"
              step="0.05"
              value={settings.rate}
              style={{ '--fill': `${((settings.rate - 0.5) / 1) * 100}%` } as React.CSSProperties}
              onChange={(e) => change({ rate: Number(e.target.value) })}
            />
          </label>
          <label className="settings-field">
            <span className="settings-label">
              <SkillIcon skill="goal" size={20} />
              {t('goal')}
            </span>
            <span className="settings-control after">
              <input
                type="number"
                min="1"
                max="120"
                value={settings.dailyGoal}
                onChange={(e) => {
                  const n = Number(e.target.value);
                  if (n >= 1 && n <= 120) change({ dailyGoal: Math.round(n) });
                }}
              />
              <SkillIcon skill="clock" size={20} />
            </span>
          </label>
          <label className="checkbox settings-check">
            <input
              type="checkbox"
              checked={settings.transcript}
              onChange={(e) => change({ transcript: e.target.checked })}
            />
            {t('transcript')}
          </label>
        </div>
        <div className="settings-column">
          <label className="settings-field">
            <span className="settings-label">
              <SkillIcon skill="speaker" size={20} />
              {t('accent')}
            </span>
            <span className="settings-control">
              <Flag code={settings.accent === 'en-US' ? 'us' : 'en'} />
              <select
                value={settings.accent}
                onChange={(e) => change({ accent: e.target.value as 'en-US' | 'en-GB' })}
              >
                <option value="en-US">American English</option>
                <option value="en-GB">British English</option>
              </select>
            </span>
          </label>
          <label className="settings-field">
            <span className="settings-label">
              <SkillIcon skill="palette" size={20} />
              {t('theme')}
            </span>
            <span className="settings-control">
              <span className="settings-theme-icon" aria-hidden="true">
                <SkillIcon skill={settings.theme === 'dark' ? 'moon' : 'sun'} size={20} />
              </span>
              <select
                value={settings.theme}
                onChange={(e) => change({ theme: e.target.value as 'light' | 'dark' })}
              >
                <option value="light">{t('light')}</option>
                <option value="dark">{t('dark')}</option>
              </select>
            </span>
          </label>
          <div className="settings-tip">
            <svg className="settings-bulb" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M9 18h6 M10 21h4 M12 3a6 6 0 0 0-3.5 10.9c.6.4 1 1.1 1 1.8V16h5v-.3c0-.7.4-1.4 1-1.8A6 6 0 0 0 12 3z" />
            </svg>
            <p>
              {bi(
                'Học từ vựng không giới hạn mỗi ngày. Mục tiêu phút học chỉ để theo dõi tiến độ.',
                'Vocabulary practice has no daily limit. Your daily minute goal only tracks progress.',
              )}
            </p>
            <svg className="settings-chart" viewBox="0 0 48 40" aria-hidden="true">
              <rect x="4" y="26" width="7" height="12" rx="1.5" />
              <rect x="15" y="20" width="7" height="18" rx="1.5" />
              <rect x="26" y="14" width="7" height="24" rx="1.5" />
              <rect x="37" y="8" width="7" height="30" rx="1.5" />
              <path d="M3 22 L16 13 L24 17 L42 3 M35 3h7v7" />
            </svg>
          </div>
        </div>
      </section>
      <section className="panel settings-data">
        <div className="settings-data-body">
          <h2>
            <span className="settings-shield" aria-hidden="true">
              <SkillIcon skill="shield" size={22} />
            </span>
            {t('data')}
          </h2>
          <p className="muted">{t('backupNote')}</p>
          <div className="actions">
            <button
              onClick={() =>
                void run(async () =>
                  download('englishup-backup.json', JSON.stringify(await exportData(), null, 2)),
                )
              }
            >
              <SkillIcon skill="download" size={18} />
              {t('export')}
            </button>
            <label className="button">
              <SkillIcon skill="upload" size={18} />
              {t('import')}
              <input
                className="sr-only"
                aria-label={t('import')}
                type="file"
                accept=".json,application/json"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file)
                    void (async () => {
                      try {
                        setPending(backupSchema.parse(JSON.parse(await file.text())));
                        setError(false);
                        setMessage('valid');
                      } catch {
                        setPending(undefined);
                        setError(true);
                        setMessage('invalid');
                      }
                    })();
                  e.target.value = '';
                }}
              />
            </label>
            <button className="danger" onClick={() => setReset(true)}>
              <SkillIcon skill="trash" size={18} />
              {t('reset')}
            </button>
          </div>
        </div>
        <img
          className="settings-data-art"
          src="/art/data-safe.webp"
          width={194}
          height={126}
          alt=""
          draggable={false}
        />
        {pending !== undefined && (
          <div className="notice">
            <p>{t('restoreConfirm')}</p>
            <button
              onClick={() =>
                void run(async () => {
                  await importData(pending);
                  await load();
                  bump();
                  setPending(undefined);
                })
              }
            >
              {t('confirm')}
            </button>{' '}
            <button onClick={() => setPending(undefined)}>{t('cancel')}</button>
          </div>
        )}
        {reset && (
          <div className="notice">
            <label>
              {t('resetConfirm')}
              <input value={confirmation} onChange={(e) => setConfirmation(e.target.value)} />
            </label>
            <button
              className="danger"
              disabled={confirmation !== 'RESET'}
              onClick={() =>
                void run(async () => {
                  await resetData();
                  await load();
                  bump();
                  setReset(false);
                  setConfirmation('');
                })
              }
            >
              {t('confirm')}
            </button>{' '}
            <button onClick={() => setReset(false)}>{t('cancel')}</button>
          </div>
        )}
        {message && (
          <Notice error={error}>
            {message === 'valid'
              ? bi(
                  'Bản sao lưu hợp lệ. Xác nhận bên dưới để khôi phục.',
                  'Valid backup. Confirm below to restore.',
                )
              : message === 'invalid'
                ? bi(
                    'Tệp sao lưu không hợp lệ hoặc không đúng phiên bản.',
                    'Invalid backup file or unsupported version.',
                  )
                : t(message)}
          </Notice>
        )}
      </section>
    </>
  );
}
