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
import { languageVocabulary, vocabularyTopics } from '../../data/languageVocabulary';
import { LessonContinue } from '../../components/LessonContinue';
import { nextLesson } from '../../services/lessonNavigation';
import LanguageVocabulary from './LanguageVocabulary';
import '../../styles/vibrant-languages.css';

const skillMarks: Record<Skill, string> = {
  vocabulary: 'Aa',
  listening: '◉',
  speaking: '◌',
  reading: '▤',
  writing: '✎',
};

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
        eyebrow={`${name.native} · ${bi('KHÔNG GIAN HỌC CỦA BẠN', 'YOUR LEARNING SPACE')}`}
        title={skill ? `${t(skill)} · ${name[settings.language]}` : name[settings.language]}
        description={
          language === 'ja'
            ? bi(
                'Từ những nét chữ đầu tiên đến những cuộc trò chuyện mỗi ngày.',
                'From your first characters to everyday conversations.',
              )
            : bi(
                'Khám phá chữ giản thể, pinyin và những từ gần gũi mỗi ngày.',
                'Discover simplified characters, pinyin and words for everyday life.',
              )
        }
      />
      {!skill ? (
        <>
          <section className="language-welcome">
            <div className="language-welcome-copy">
              <span className="language-kicker">
                {bi('MỖI NGÀY, THÊM MỘT CHÚT', 'A LITTLE MORE, EVERY DAY')}
              </span>
              <h2>
                {bi('Một từ mới.', 'One new word.')}
                <br />
                <em>{bi('Một thế giới rộng hơn.', 'A wider world.')}</em>
              </h2>
              <p>
                {bi(
                  `${words.length.toLocaleString('vi-VN')} từ thông dụng, chia theo chủ đề. Có phiên âm, nghĩa và giọng đọc để bạn bắt đầu thật nhẹ nhàng.`,
                  `${words.length.toLocaleString('en-US')} everyday words, organized by topic. Explore their readings, meanings and pronunciation at your own pace.`,
                )}
              </p>
              <Link className="button primary" to="/vocabulary">
                {bi('Khám phá từ vựng', 'Explore vocabulary')} <span aria-hidden="true">↗</span>
              </Link>
              <small>
                {bi(
                  'Học theo nhịp của bạn · Lưu trên thiết bị',
                  'Your pace · Saved on your device',
                )}
              </small>
            </div>
            <div className="language-welcome-art" aria-hidden="true">
              <div className="language-art-ring" />
              <div className="language-art-page language-art-back">
                <span>{name.native}</span>
                <i>{language === 'ja' ? '学ぶ' : '学习'}</i>
              </div>
              <div className="language-art-page language-art-front">
                <span>{bi('MỖI CHỮ, MỘT KHỞI ĐẦU', 'EVERY WORD, A BEGINNING')}</span>
                <strong lang={language}>{name.mark}</strong>
                <small>{language === 'ja' ? 'nihongo' : 'zhōngwén'}</small>
              </div>
              <div className="language-art-note">
                <strong lang={language}>{language === 'ja' ? 'こんにちは' : '你好'}</strong>
                <span>{language === 'ja' ? 'konnichiwa' : 'nǐ hǎo'}</span>
                <small>
                  {bi('Xin chào', 'Hello')} <span>✦</span>
                </small>
              </div>
              <span className="language-art-spark">✳</span>
            </div>
          </section>
          <div className="language-summary">
            <div>
              <strong>
                {words.length.toLocaleString(settings.language === 'vi' ? 'vi-VN' : 'en-US')}
              </strong>
              <span>{bi('từ thông dụng để khám phá', 'everyday words to discover')}</span>
            </div>
            <div>
              <strong>{vocabularyTopics.length.toString().padStart(2, '0')}</strong>
              <span>{bi('chủ đề gần gũi với bạn', 'topics from everyday life')}</span>
            </div>
            <div>
              <strong>{attempts.length.toString().padStart(2, '0')}</strong>
              <span>{bi('lượt luyện tập đã lưu', 'saved practice attempts')}</span>
            </div>
          </div>
          <section className="language-discover">
            <div className="language-section-heading">
              <div>
                <p className="eyebrow">
                  {bi('BẮT ĐẦU TỪ ĐIỀU QUEN THUỘC', 'START WITH THE FAMILIAR')}
                </p>
                <h2>{bi('Hôm nay, bạn muốn khám phá gì?', 'What will you discover today?')}</h2>
              </div>
              <Link className="text-link" to="/vocabulary">
                {bi('Tất cả chủ đề', 'All topics')} <span aria-hidden="true">↗</span>
              </Link>
            </div>
            <div className="language-topic-grid">
              {vocabularyTopics.slice(0, 6).map((topic) => (
                <Link
                  className="language-topic-card"
                  data-topic={topic.id}
                  key={topic.id}
                  to={`/vocabulary?topic=${encodeURIComponent(topic.id)}`}
                >
                  <span className="language-topic-mark" aria-hidden="true">
                    {topic.mark}
                  </span>
                  <strong>{topic[settings.language]}</strong>
                  <span>
                    {words.filter((word) => word.topic === topic.id).length}{' '}
                    {bi('từ vựng', 'words')} <i aria-hidden="true">↗</i>
                  </span>
                </Link>
              ))}
            </div>
          </section>
          <section className="language-skills">
            <div className="language-section-heading">
              <div>
                <p className="eyebrow">{bi('THỬ MỘT CHÚT MỖI NGÀY', 'MAKE A LITTLE TIME')}</p>
                <h2>{bi('Đưa ngôn ngữ vào cuộc sống', 'Bring the language to life')}</h2>
              </div>
              <span className="muted">{bi('Bài luyện nhập môn', 'Starter practice')}</span>
            </div>
            <div className="language-skill-grid">
              {skills
                .filter((item) => item !== 'vocabulary')
                .map((item) => (
                  <Link className="language-card" data-skill={item} key={item} to={`/${item}`}>
                    <span className="language-skill-mark" aria-hidden="true">
                      {skillMarks[item]}
                    </span>
                    <h3>{t(item)}</h3>
                    <p>
                      {lessons.length} {bi('bài nhập môn', 'starter lessons')}
                    </p>
                    <span className="language-card-arrow" aria-hidden="true">
                      ↗
                    </span>
                  </Link>
                ))}
            </div>
          </section>
          <section className="panel language-history">
            <div className="language-section-heading">
              <h2>{bi('Những bước tiến gần đây', 'Your recent steps')}</h2>
              <span className="badge">{bi('Đã lưu trên thiết bị', 'Saved on this device')}</span>
            </div>
            {error && <p role="alert">{error}</p>}
            {attempts.length === 0 ? (
              <div className="language-history-empty">
                <span aria-hidden="true">✦</span>
                <p>
                  {bi(
                    'Trang đầu tiên đang chờ bạn. Hoàn thành một bài luyện để ghi lại bước tiến của mình.',
                    'Your first page is waiting. Complete a practice to see your progress here.',
                  )}
                </p>
                <Link className="text-link" to="/vocabulary">
                  {bi('Bắt đầu với một từ mới', 'Start with a new word')} →
                </Link>
              </div>
            ) : (
              <ul className="language-history-list">
                {attempts.slice(0, 10).map((attempt) => (
                  <li key={attempt.id}>
                    <span className="language-skill-mark" aria-hidden="true">
                      {skillMarks[attempt.skill]}
                    </span>
                    <div>
                      <strong>{attempt.label}</strong>
                      <small>
                        {t(attempt.skill)} ·{' '}
                        {new Date(attempt.timestamp).toLocaleDateString(
                          settings.language === 'vi' ? 'vi-VN' : 'en-US',
                        )}
                      </small>
                    </div>
                    <span className="badge">{attempt.score}%</span>
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
