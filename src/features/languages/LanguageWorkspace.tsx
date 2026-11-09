import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useBi, useT } from '../../i18n';
import { PageTitle, useLive } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import { languageLessons, languageNames, type LanguageLesson } from '../../data/languages';
import type { Skill } from '../../data/schema';
import { db } from '../../services/storage';
import { skills } from '../../services/progress';
import { speak, stopSpeech } from '../../services/speech';
import { matchesModel, saveLanguagePractice } from '../../services/languages';
import { languageVocabulary, vocabularyTopics } from '../../data/languageVocabulary';
import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import LanguageVocabulary from './LanguageVocabulary';
import '../../styles/vibrant-languages.css';

export default function LanguageWorkspace({ skill }: { skill?: Skill }) {
  const { settings } = useApp();
  const bi = useBi();
  const t = useT();
  const language = settings.learningLanguage;
  const name = languageNames[language];
  const lessons = languageLessons.filter((lesson) => lesson.language === language);
  const words = languageVocabulary.filter((word) => word.language === language);
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
  if (skill === 'vocabulary' && language !== 'en') {
    return (
      <div className={`language-space language-${language}`}>
        <LanguageVocabulary language={language} />
      </div>
    );
  }
  return (
    <div className={`language-space language-${language}`}>
      <PageTitle
        title={skill ? `${t(skill)} · ${name[settings.language]}` : name[settings.language]}
      />
      {!skill ? (
        <div className="home-grid">
          <section className="panel" aria-labelledby="topics-title">
            <div className="panel-head">
              <h2 id="topics-title">{bi('Từ vựng theo chủ đề', 'Words by topic')}</h2>
              <Link className="text-link" to="/vocabulary">
                {bi('Tất cả chủ đề', 'All topics')}
              </Link>
            </div>
            <ul className="line-list" data-skill="vocabulary">
              {vocabularyTopics.slice(0, 6).map((topic) => (
                <li key={topic.id}>
                  <Link to={`/vocabulary?topic=${encodeURIComponent(topic.id)}`}>
                    <span className="line-tile" aria-hidden="true" lang={language}>
                      {topic.mark}
                    </span>
                    <span className="line-name">
                      <strong>{topic[settings.language]}</strong>
                      <small>
                        {words.filter((word) => word.topic === topic.id).length} {bi('từ', 'words')}
                      </small>
                    </span>
                    <SkillIcon skill="arrow" size={18} />
                  </Link>
                </li>
              ))}
            </ul>
          </section>
          <div className="home-side">
            <section className="panel" aria-labelledby="starter-title">
              <h2 id="starter-title">{bi('Bài nhập môn', 'Starter lessons')}</h2>
              <ul className="line-list">
                {skills
                  .filter((item) => item !== 'vocabulary' && item !== 'grammar')
                  .map((item) => (
                    <li key={item} data-skill={item}>
                      <Link to={`/${item}`}>
                        <span className="line-tile" aria-hidden="true">
                          <SkillIcon skill={item} />
                        </span>
                        <span className="line-name">
                          <strong>{t(item)}</strong>
                          <small>
                            {lessons.length} {bi('bài', 'lessons')}
                          </small>
                        </span>
                        <SkillIcon skill="arrow" size={18} />
                      </Link>
                    </li>
                  ))}
              </ul>
            </section>
            <section className="panel" aria-labelledby="history-title">
              <h2 id="history-title">{t('recent')}</h2>
              {error && <p role="alert">{error}</p>}
              {attempts.length === 0 ? (
                <p className="muted">{t('noActivity')}</p>
              ) : (
                <ul className="recent-list">
                  {attempts.slice(0, 10).map((attempt) => (
                    <li key={attempt.id} data-skill={attempt.skill}>
                      <span className="line-tile small" aria-hidden="true">
                        <SkillIcon skill={attempt.skill} size={16} />
                      </span>
                      <span className="recent-text">
                        <strong>{attempt.label}</strong>
                        <small>
                          {t(attempt.skill)} ·{' '}
                          {new Date(attempt.timestamp).toLocaleDateString(
                            settings.language === 'vi' ? 'vi-VN' : 'en-US',
                          )}
                        </small>
                      </span>
                      <span className="badge">{attempt.score}%</span>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        </div>
      ) : active ? (
        <Practice
          key={`${active.id}-${skill}`}
          lesson={active}
          skill={skill}
          onBack={() => setActive(undefined)}
          onContinue={() => setActive(nextLesson(lessons, active))}
          hasNext={!!nextLesson(lessons, active)}
        />
      ) : (
        <div className="language-grid">
          {lessons.map((lesson, index) => (
            <article className="panel language-lesson" key={lesson.id}>
              <span className="language-kicker">
                {bi('BÀI', 'LESSON')} {(index + 1).toString().padStart(2, '0')}
              </span>
              <h2>{lesson.title[settings.language]}</h2>
              <p className="language-lesson-script" lang={language}>
                {lesson.text}
              </p>
              <p className="muted">{lesson.romanization}</p>
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
  onContinue,
  hasNext,
}: {
  lesson: LanguageLesson;
  skill: Skill;
  onBack: () => void;
  onContinue: () => void;
  hasNext: boolean;
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
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => {
    heading.current?.focus();
    return () => stopSpeech();
  }, []);
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
      <h2 ref={heading} tabIndex={-1}>
        {lesson.title[locale]}
      </h2>
      {skill !== 'listening' && (
        <p className="target-script" lang={skill === 'writing' ? locale : lesson.language}>
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
        <div className="language-result">
          <div role="status">
            <h3>
              {bi('Đã lưu bài luyện tập', 'Practice saved')} · {score}%
            </h3>
            <p>
              {skill === 'speaking'
                ? bi('Điểm hoàn thành tự đánh giá', 'Self-assessed completion score')
                : bi('Đáp án mẫu', 'Model answer')}
            </p>
            <p lang={skill === 'reading' ? locale : lesson.language}>
              {skill === 'reading' ? lesson.options[lesson.answer][locale] : lesson.text}
            </p>
            <p>
              {lesson.romanization} · {lesson.meaning[locale]}
            </p>
          </div>
          <LessonContinue onContinue={onContinue} hasNext={hasNext} />
        </div>
      )}
    </section>
  );
}
