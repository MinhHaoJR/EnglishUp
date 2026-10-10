import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useBi } from '../../i18n';
import { languageNames } from '../../data/languages';
import { learningLanguageSchema } from '../../services/storage';
import { stopSpeech } from '../../services/speech';
export default function LanguagePicker() {
  const { settings, update, filter } = useApp();
  const bi = useBi();
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  return (
    <div className={`language-picker picker-${settings.learningLanguage}`} aria-busy={busy}>
      <div className="language-picker-heading">
        <label htmlFor="learning-language">{bi('Ngôn ngữ muốn học', 'Learning language')}</label>
        <span className="language-picker-mark" aria-hidden="true">
          {languageNames[settings.learningLanguage].mark}
        </span>
      </div>
      <select
        id="learning-language"
        value={settings.learningLanguage}
        disabled={busy}
        onChange={async (event) => {
          const learningLanguage = learningLanguageSchema.parse(event.target.value);
          setBusy(true);
          setError(false);
          stopSpeech();
          try {
            await update({ learningLanguage });
            filter('all', 'all');
            navigate('/');
          } catch {
            setError(true);
          } finally {
            setBusy(false);
          }
        }}
      >
        {Object.entries(languageNames).map(([code, name]) => (
          <option key={code} value={code}>
            {name[settings.language]} · {name.native}
          </option>
        ))}
      </select>
      <p className="language-picker-note">
        {bi('Một góc nhỏ, ba ngôn ngữ', 'A little space, three languages')}
      </p>
      {error && (
        <p role="alert">
          {bi('Không lưu được lựa chọn. Hãy thử lại.', 'Could not save your choice. Please retry.')}
        </p>
      )}
    </div>
  );
}
