import { useEffect, useId, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useBi } from '../../i18n';
import SkillIcon from '../../components/SkillIcon';
import { Flag } from '../../components/Flag';
import { languageNames } from '../../data/languages';
import { learningLanguageSchema, type LearningLanguage } from '../../services/storage';
import { stopSpeech } from '../../services/speech';

const codes = learningLanguageSchema.options;

/** The learning language as a select-only combobox (WAI-ARIA pattern): flag, name, then a list with a check. */
export default function LanguagePicker() {
  const { settings, update, filter } = useApp();
  const bi = useBi();
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const root = useRef<HTMLDivElement>(null);
  const box = useRef<HTMLDivElement>(null);
  const id = useId();
  const current = settings.learningLanguage;
  const label = (code: LearningLanguage) =>
    `${languageNames[code][settings.language]} · ${languageNames[code].native}`;

  useEffect(() => {
    if (!open) return;
    const close = (event: PointerEvent) => {
      if (!root.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener('pointerdown', close);
    return () => document.removeEventListener('pointerdown', close);
  }, [open]);

  function show() {
    setActive(codes.indexOf(current));
    setOpen(true);
  }

  async function choose(code: LearningLanguage) {
    setOpen(false);
    box.current?.focus();
    if (code === current) return;
    setBusy(true);
    setError(false);
    stopSpeech();
    try {
      await update({ learningLanguage: code });
      filter('all', 'all');
      navigate('/');
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  function keyDown(event: React.KeyboardEvent) {
    if (busy) return;
    const last = codes.length - 1;
    const keys: Record<string, () => void> = open
      ? {
          ArrowDown: () => setActive(Math.min(active + 1, last)),
          ArrowUp: () => setActive(Math.max(active - 1, 0)),
          Home: () => setActive(0),
          End: () => setActive(last),
          Enter: () => void choose(codes[active]),
          ' ': () => void choose(codes[active]),
          Escape: () => setOpen(false),
        }
      : { ArrowDown: show, ArrowUp: show, Enter: show, ' ': show };
    if (event.key === 'Tab') setOpen(false);
    else if (keys[event.key]) {
      event.preventDefault();
      keys[event.key]();
    }
  }

  return (
    <div className="language-picker" ref={root} aria-busy={busy}>
      <div className="language-picker-heading">
        <span className="language-globe" aria-hidden="true">
          <SkillIcon skill="globe" size={15} />
        </span>
        <span id={`${id}-label`}>{bi('Đang học', 'Learning')}</span>
      </div>
      <div className="language-field">
        <div
          ref={box}
          role="combobox"
          tabIndex={0}
          className="language-current"
          aria-labelledby={`${id}-label`}
          aria-haspopup="listbox"
          aria-expanded={open}
          aria-controls={`${id}-list`}
          aria-activedescendant={open ? `${id}-${codes[active]}` : undefined}
          aria-disabled={busy || undefined}
          onClick={() => !busy && (open ? setOpen(false) : show())}
          onKeyDown={keyDown}
        >
          <Flag code={current} />
          <span className="language-text">
            <strong>{languageNames[current][settings.language]}</strong>
            <span lang={current}>{languageNames[current].native}</span>
          </span>
          <span className="language-chevron" aria-hidden="true">
            <SkillIcon skill="chevron" size={16} />
          </span>
        </div>
        {open && (
          <ul
            className="language-list"
            id={`${id}-list`}
            role="listbox"
            aria-labelledby={`${id}-label`}
          >
            {codes.map((code, i) => (
              <li
                key={code}
                id={`${id}-${code}`}
                role="option"
                aria-selected={code === current}
                aria-label={label(code)}
                className={i === active ? 'active' : undefined}
                onPointerMove={() => setActive(i)}
                onClick={() => void choose(code)}
              >
                <Flag code={code} />
                <span className="language-text">
                  <strong>{languageNames[code][settings.language]}</strong>
                  <span lang={code}>{languageNames[code].native}</span>
                </span>
                {code === current && (
                  <span className="language-check" aria-hidden="true">
                    <SkillIcon skill="check" size={14} />
                  </span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
      {error && (
        <p role="alert">
          {bi('Không lưu được lựa chọn. Hãy thử lại.', 'Could not save your choice. Please retry.')}
        </p>
      )}
    </div>
  );
}
