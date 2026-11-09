import { useState } from 'react';
import { useApp } from '../../app/store';
import { useT, useBi } from '../../i18n';
import { PageTitle, Notice } from '../../components/shared';
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
      <PageTitle title={t('settings')} />
      <section className="panel form-grid">
        <label>
          {t('language')}
          <select
            value={settings.language}
            onChange={(e) => change({ language: e.target.value as 'vi' | 'en' })}
          >
            <option value="vi">Tiếng Việt</option>
            <option value="en">English</option>
          </select>
        </label>
        <label>
          {t('accent')}
          <select
            value={settings.accent}
            onChange={(e) => change({ accent: e.target.value as 'en-US' | 'en-GB' })}
          >
            <option value="en-US">American English</option>
            <option value="en-GB">British English</option>
          </select>
        </label>
        <label>
          {t('rate')}: {settings.rate}×
          <input
            type="range"
            min="0.5"
            max="1.5"
            step="0.05"
            value={settings.rate}
            onChange={(e) => change({ rate: Number(e.target.value) })}
          />
        </label>
        <label>
          {t('theme')}
          <select
            value={settings.theme}
            onChange={(e) => change({ theme: e.target.value as 'light' | 'dark' })}
          >
            <option value="light">{t('light')}</option>
            <option value="dark">{t('dark')}</option>
          </select>
        </label>
        <label>
          {t('goal')}
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
        </label>
        <div className="notice">
          {bi(
            'Học từ vựng không giới hạn mỗi ngày. Mục tiêu phút học chỉ để theo dõi tiến độ.',
            'Vocabulary practice has no daily limit. Your daily minute goal only tracks progress.',
          )}
        </div>
        <label className="checkbox">
          <input
            type="checkbox"
            checked={settings.transcript}
            onChange={(e) => change({ transcript: e.target.checked })}
          />
          {t('transcript')}
        </label>
      </section>
      <section className="panel space-y-4">
        <h2>{t('data')}</h2>
        <p className="muted">{t('backupNote')}</p>
        <div className="actions">
          <button
            onClick={() =>
              void run(async () =>
                download('englishup-backup.json', JSON.stringify(await exportData(), null, 2)),
              )
            }
          >
            {t('export')}
          </button>
          <label className="button">
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
            {t('reset')}
          </button>
        </div>
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
