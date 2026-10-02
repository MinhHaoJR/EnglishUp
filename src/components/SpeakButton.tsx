import { useEffect, useState } from 'react';
import { useApp } from '../app/store';
import { useT } from '../i18n';
import { speak, stopSpeech } from '../services/speech';
export function SpeakButton({ text }: { text: string }) {
  const settings = useApp((s) => s.settings);
  const t = useT();
  const [error, setError] = useState(false);
  useEffect(() => () => stopSpeech(), []);
  return (
    <>
      <button
        type="button"
        onClick={() => setError(!speak(text, settings, 0, () => setError(true)))}
      >
        ◖)) {t('listen')}
      </button>
      {error && (
        <span role="status" className="muted">
          {t('unsupported')}
        </span>
      )}
    </>
  );
}
