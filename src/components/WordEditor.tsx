import { useState } from 'react';
import { wordSchema, levelSchema, type Word, type Level } from '../data/schema';
import { topics, topicVi, useT, useBi } from '../i18n';
import { db } from '../services/storage';
import { Notice } from './shared';
export function WordEditor({ word, onClose }: { word?: Partial<Word>; onClose: () => void }) {
  const t = useT();
  const bi = useBi();
  const [form, setForm] = useState({
    word: word?.word ?? '',
    ipa: word?.ipa ?? '',
    pos: word?.pos ?? 'noun',
    meaning: word?.meaning ?? '',
    definition: word?.definition ?? '',
    examples: word?.examples?.join('\n') ?? '',
    level: word?.level ?? 'A2',
    topic: word?.topic ?? 'Daily life',
  });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  return (
    <form
      className="panel form-grid"
      onSubmit={(e) => {
        e.preventDefault();
        setBusy(true);
        void (async () => {
          try {
            const parsed = wordSchema.parse({
              ...form,
              id: word?.custom && word.id ? word.id : crypto.randomUUID(),
              examples: form.examples.split('\n').filter(Boolean),
              custom: true,
              updated: Date.now(),
            });
            await db.words.put(parsed);
            onClose();
          } catch {
            setError(
              bi(
                'Vui lòng điền đầy đủ, gồm 1–2 câu ví dụ.',
                'Please fill all fields, including 1–2 examples.',
              ),
            );
          } finally {
            setBusy(false);
          }
        })();
      }}
    >
      <h2 className="col-span-full">{word?.id ? t('edit') : t('add')}</h2>
      {(
        [
          ['word', bi('Từ / cụm từ', 'Word / phrase')],
          ['ipa', 'IPA'],
          ['pos', bi('Từ loại', 'Part of speech')],
          ['meaning', bi('Nghĩa tiếng Việt', 'Vietnamese meaning')],
          ['definition', 'English definition'],
        ] as const
      ).map(([key, label]) => (
        <label key={key}>
          {label}
          <input
            required={key !== 'ipa'}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        </label>
      ))}
      <label>
        {bi('Ví dụ (mỗi dòng một câu, tối đa 2)', 'Examples (one per line, up to 2)')}
        <textarea
          required
          value={form.examples}
          onChange={(e) => setForm({ ...form, examples: e.target.value })}
        />
      </label>
      <label>
        {t('level')}
        <select
          value={form.level}
          onChange={(e) => setForm({ ...form, level: e.target.value as Level })}
        >
          {levelSchema.options.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>
      </label>
      <label>
        {t('topic')}
        <select value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })}>
          {[...new Set([...topics, form.topic])].map((topic) => (
            <option key={topic} value={topic}>
              {bi(topicVi[topic] ?? topic, topic)}
            </option>
          ))}
        </select>
      </label>
      <div className="actions col-span-full">
        <button className="primary" disabled={busy}>
          {t('save')}
        </button>
        <button type="button" onClick={onClose}>
          {t('cancel')}
        </button>
      </div>
      {error && <Notice error>{error}</Notice>}
    </form>
  );
}
