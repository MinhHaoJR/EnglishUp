import { useState } from 'react';
import { vocabulary } from '../data/content';
import { db } from '../services/storage';
import { useBi, useT } from '../i18n';
import { WordEditor } from './WordEditor';
import { useLive, Notice } from './shared';
import { SpeakButton } from './SpeakButton';
export function DictionaryText({ text }: { text: string }) {
  const t = useT();
  const bi = useBi();
  const [selected, setSelected] = useState('');
  const [manual, setManual] = useState(false);
  const [message, setMessage] = useState('');
  const { value: custom = [] } = useLive(() => db.words.toArray());
  const normalized = selected.toLowerCase();
  const word = [...custom, ...vocabulary].find((w) => w.word.toLowerCase() === normalized);
  return (
    <>
      <div className="prose">
        {/* Each word keeps its punctuation on the same line ("started." never wraps before the dot). */}
        {text.split(/(\s+)/).map((chunk, i) =>
          /^\s*$/.test(chunk) ? (
            chunk
          ) : (
            <span className="whitespace-nowrap" key={i}>
              {chunk.split(/([A-Za-z]+(?:['’][A-Za-z]+)?)/).map((part, j) =>
                /^[A-Za-z]/.test(part) ? (
                  <button
                    className="word-button"
                    key={j}
                    onClick={() => {
                      setSelected(part);
                      setManual(false);
                      setMessage('');
                    }}
                    aria-label={`${bi('Tra từ', 'Look up')} ${part}`}
                  >
                    {part}
                  </button>
                ) : (
                  part
                ),
              )}
            </span>
          ),
        )}
      </div>
      {selected && (
        <section className="dictionary-box" aria-label={bi('Tra từ', 'Dictionary')}>
          <div className="flex justify-between items-center">
            <h3>{selected}</h3>
            <button
              aria-label={bi('Đóng tra từ', 'Close dictionary')}
              onClick={() => setSelected('')}
            >
              ×
            </button>
          </div>
          {word ? (
            <>
              <p>
                {word.ipa} · {word.pos}
              </p>
              <strong>{word.meaning}</strong>
              <p>{word.definition}</p>
              <div className="actions">
                <SpeakButton text={word.word} />
                <button
                  onClick={() =>
                    void (async () => {
                      try {
                        if (custom.some((w) => w.word.toLowerCase() === normalized)) {
                          setMessage(
                            bi(
                              'Từ này đã có trong sổ của bạn.',
                              'This word is already in your collection.',
                            ),
                          );
                          return;
                        }
                        await db.words.add({ ...word, id: crypto.randomUUID(), custom: true });
                        setMessage(t('saved'));
                      } catch {
                        setMessage(t('error'));
                      }
                    })()
                  }
                >
                  {t('add')}
                </button>
              </div>
            </>
          ) : (
            <>
              <p className="muted">
                {bi(
                  'Chưa có trong từ điển cục bộ. Thêm nghĩa và ví dụ để lưu.',
                  'Not in the bundled dictionary. Add a meaning and example to save it.',
                )}
              </p>
              <button onClick={() => setManual(true)}>{t('add')}</button>
            </>
          )}
          {message && <Notice>{message}</Notice>}
          {manual && (
            <WordEditor
              word={{ word: normalized }}
              onClose={() => {
                setManual(false);
                setMessage(t('saved'));
              }}
            />
          )}
        </section>
      )}
    </>
  );
}
