import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useBi, useT } from '../../i18n';
import { PageTitle, useLive } from '../../components/shared';
import { languageLessons, languageNames, type LanguageLesson } from '../../data/languages';
import type { Skill } from '../../data/schema';
import { db } from '../../services/storage';
import { skills } from '../../services/progress';
import { speak, stopSpeech } from '../../services/speech';
import { matchesModel, saveLanguagePractice } from '../../services/languages';
export default function LanguageWorkspace({ skill }: { skill?: Skill }) {
  const { settings } = useApp();
  const bi = useBi();
  const t = useT();
  const language = settings.learningLanguage;
  const name = languageNames[language];
  const lessons = languageLessons.filter((lesson) => lesson.language === language);
  const [active, setActive] = useState<LanguageLesson>();
  const { value: attempts = [], error } = useLive(
    () =>
      db.attempts
        .orderBy('timestamp')
        .reverse()
        .filter((attempt) => attempt.learningLanguage === language)
        .toArray(),
    [language],
  );
  return (
    <div className={`language-space language-${language}`}>
      <PageTitle
        eyebrow={`${name.native} · ${bi('Nhập môn', 'Beginner')}`}
        title={skill ? `${t(skill)} · ${name[settings.language]}` : name[settings.language]}
        description={
          language === 'ja'
            ? bi(
                'Làm quen với chữ Nhật, romaji và giao tiếp cơ bản.',
                'Explore Japanese script, romaji and everyday phrases.',
              )
            : bi(
                'Bắt đầu với chữ giản thể, pinyin và hội thoại phổ thông.',
                'Start with simplified characters, pinyin and Mandarin phrases.',
              )
        }
      />
      {!skill ? (
        <>
          <section className="language-banner">
            <span aria-hidden="true">{name.mark}</span>
            <div>
              <h2>{bi('Một ngôn ngữ mới, một khởi đầu mới', 'A new language, a fresh start')}</h2>
              <p>
                {bi(
                  'Chọn một kỹ năng để bắt đầu bài học ngắn mỗi ngày.',
                  'Choose a skill for a short daily lesson.',
                )}
              </p>
              <p>
                {attempts.length} {bi('lượt luyện tập đã lưu', 'saved practice attempts')}
              </p>
            </div>
          </section>
          <div className="language-grid">
            {skills.map((item) => (
              <Link className="panel language-card" key={item} to={`/${item}`}>
                <h2>{t(item)} →</h2>
                <p>
                  {lessons.length} {bi('bài nhập môn', 'starter lessons')}
                </p>
              </Link>
            ))}
          </div>
          <section className="panel">
            <h2>{bi('Lịch sử học', 'Learning history')}</h2>
            {error && <p role="alert">{error}</p>}
            {attempts.length === 0 ? (
              <p>{bi('Chưa có lượt luyện tập.', 'No practice yet.')}</p>
            ) : (
              <ul>
                {attempts.slice(0, 10).map((attempt) => (
                  <li key={attempt.id}>
                    {t(attempt.skill)} · {attempt.label} · {attempt.score}%
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      ) : active ? (
        <Practice
          key={`${active.id}-${skill}`}
          lesson={active}
          skill={skill}
          onBack={() => setActive(undefined)}
        />
      ) : (
        <div className="language-grid">
          {lessons.map((lesson) => (
            <article className="panel" key={lesson.id}>
              <h2>{lesson.title[settings.language]}</h2>
              <p lang={language}>{lesson.text}</p>
              <p>{lesson.romanization}</p>
              <button onClick={() => setActive(lesson)}>{t('start')}</button>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
function Practice({
  lesson,
  skill,
  onBack,
}: {
  lesson: LanguageLesson;
  skill: Skill;
  onBack: () => void;
}) {
  const { settings } = useApp();
  const bi = useBi();
  const t = useT();
  const [answer, setAnswer] = useState('');
  const [choice, setChoice] = useState<number>();
  const [confirmed, setConfirmed] = useState(false);
  const [score, setScore] = useState<number>();
  const [error, setError] = useState('');
  const [audioError, setAudioError] = useState(false);
  const [busy, setBusy] = useState(false);
  const saving = useRef(false);
  const started = useRef(Date.now());
  useEffect(() => () => stopSpeech(), []);
  const locale = settings.language;
  const isChoice = skill === 'reading' || skill === 'vocabulary';
  const options =
    skill === 'reading' ? lesson.options : [lesson.meaning, { vi: 'Tạm biệt', en: 'Goodbye' }];
  async function submit() {
    if (saving.current || score !== undefined) return;
    saving.current = true;
    setBusy(true);
    setError('');
    const result =
      skill === 'speaking'
        ? 100
        : isChoice
          ? choice === (skill === 'reading' ? lesson.answer : 0)
            ? 100
            : 0
          : matchesModel(answer, lesson.text)
            ? 100
            : 0;
    try {
      await saveLanguagePractice(lesson, skill, result, started.current, answer);
      setScore(result);
    } catch {
      setError(bi('Không lưu được bài. Hãy thử lại.', 'Could not save. Please retry.'));
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }
  return (
    <section className="panel language-practice">
      <button onClick={onBack} disabled={busy}>
        {bi('← Danh sách bài', '← Lessons')}
      </button>
      <h2>{lesson.title[locale]}</h2>
      {skill !== 'listening' && (
        <p className="target-script" lang={lesson.language}>
          {skill === 'reading'
            ? lesson.passage
            : skill === 'writing'
              ? lesson.meaning[locale]
              : lesson.text}
        </p>
      )}
      {(skill === 'vocabulary' || skill === 'speaking') && <p>{lesson.romanization}</p>}
      {skill === 'listening' && (
        <p>
          {bi(
            'Nghe và nhập lại câu bằng chữ của ngôn ngữ đang học.',
            'Listen and type the phrase in the target script.',
          )}
        </p>
      )}
      <button
        onClick={() =>
          setAudioError(
            !speak(
              skill === 'reading' ? lesson.passage : lesson.text,
              { accent: lesson.language === 'ja' ? 'ja-JP' : 'zh-CN', rate: settings.rate },
              0,
              () => setAudioError(true),
            ),
          )
        }
      >
        {t('listen')}
      </button>
      {audioError && (
        <p role="status">
          {bi(
            'Trình duyệt chưa có giọng đọc phù hợp. Bạn có thể chọn bài khác.',
            'A suitable voice is unavailable. You can choose another lesson.',
          )}
        </p>
      )}
      {isChoice ? (
        <fieldset disabled={score !== undefined || busy}>
          <legend>
            {skill === 'reading'
              ? lesson.question[locale]
              : bi('Chọn nghĩa đúng', 'Choose the meaning')}
          </legend>
          {options.map((option, index) => (
            <label key={index} className="language-option">
              <input
                type="radio"
                name="answer"
                checked={choice === index}
                onChange={() => setChoice(index)}
              />{' '}
              {option[locale]}
            </label>
          ))}
        </fieldset>
      ) : skill === 'speaking' ? (
        <>
          <p>
            {bi(
              'Nghe mẫu và đọc thành tiếng. Bài này tự đánh giá, không chấm phát âm tự động.',
              'Listen and speak aloud. This is self-assessment, not automatic pronunciation scoring.',
            )}
          </p>
          <label>
            <input
              type="checkbox"
              disabled={score !== undefined || busy}
              checked={confirmed}
              onChange={(event) => setConfirmed(event.target.checked)}
            />{' '}
            {bi(
              'Tôi đã đọc thành tiếng và tự đối chiếu với mẫu.',
              'I practiced aloud and compared myself with the model.',
            )}
          </label>
        </>
      ) : (
        <label>
          {bi('Câu trả lời', 'Your answer')}
          <textarea
            lang={lesson.language}
            value={answer}
            disabled={score !== undefined || busy}
            onChange={(event) => setAnswer(event.target.value)}
          />
        </label>
      )}
      {skill === 'writing' && (
        <p>
          {bi(
            'Viết câu tương ứng bằng chữ Nhật/Trung. Chỉ đối chiếu với câu mẫu; chưa chấm bài viết tự do.',
            'Write the matching phrase in Japanese/Chinese script. Model comparison only; no free-writing assessment.',
          )}
        </p>
      )}
      {error && <p role="alert">{error}</p>}
      {score === undefined ? (
        <button
          className="primary"
          disabled={
            busy ||
            (isChoice ? choice === undefined : skill === 'speaking' ? !confirmed : !answer.trim())
          }
          onClick={() => void submit()}
        >
          {bi('Hoàn thành & lưu', 'Finish & save')}
        </button>
      ) : (
        <div role="status">
          <h3>
            {bi('Đã lưu bài luyện tập', 'Practice saved')} · {score}%
          </h3>
          <p>
            {skill === 'speaking'
              ? bi('Điểm hoàn thành tự đánh giá', 'Self-assessed completion score')
              : bi('Đáp án mẫu', 'Model answer')}
          </p>
          <p lang={lesson.language}>
            {skill === 'reading' ? lesson.options[lesson.answer][locale] : lesson.text}
          </p>
          <p>
            {lesson.romanization} · {lesson.meaning[locale]}
          </p>
        </div>
      )}
    </section>
  );
}
