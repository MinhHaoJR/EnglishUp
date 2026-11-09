import { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useApp } from '../../app/store';
import { useBi, useT } from '../../i18n';
import { Notice, useLive } from '../../components/shared';
import SkillIcon from '../../components/SkillIcon';
import {
  languageVocabulary,
  vocabularyTopics,
  type LanguageWord,
  type VocabularyLanguage,
} from '../../data/languageVocabulary';
import { languageNames } from '../../data/languages';
import {
  filterLanguageWords,
  vocabularyPractice,
  saveWordPractice,
  type WordQuestion,
} from '../../services/languageVocabulary';
import { db } from '../../services/storage';
import { speak, stopSpeech } from '../../services/speech';

const PAGE_SIZE = 24;

export default function LanguageVocabulary({ language }: { language: VocabularyLanguage }) {
  const bi = useBi();
  const t = useT();
  const settings = useApp((s) => s.settings);
  const [params, setParams] = useSearchParams();
  const topicParam = params.get('topic');
  const topic = vocabularyTopics.some((item) => item.id === topicParam) ? topicParam! : 'all';
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [queue, setQueue] = useState<WordQuestion[]>();
  const [audioError, setAudioError] = useState(false);
  const locale = settings.language;
  const words = useMemo(
    () => languageVocabulary.filter((word) => word.language === language),
    [language],
  );
  const filtered = useMemo(() => filterLanguageWords(words, topic, search), [words, topic, search]);
  const { value: attempts = [], error } = useLive(
    () =>
      db.attempts
        .where('skill')
        .equals('vocabulary')
        .filter((attempt) => attempt.learningLanguage === language)
        .toArray(),
    [language],
  );
  const practiced = new Set(attempts.map((attempt) => attempt.label));
  const learned = words.filter((word) => practiced.has(word.text)).length;
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const currentPage = Math.min(page, pages);
  const displayed = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);
  const resultHeading = useRef<HTMLHeadingElement>(null);
  useEffect(() => () => stopSpeech(), []);
  function listen(word: LanguageWord) {
    setAudioError(false);
    if (
      !speak(
        word.text,
        { accent: language === 'ja' ? 'ja-JP' : 'zh-CN', rate: settings.rate },
        0,
        () => setAudioError(true),
      )
    )
      setAudioError(true);
  }
  function start(first?: LanguageWord) {
    stopSpeech();
    setAudioError(false);
    setQueue(vocabularyPractice(filtered, words, first));
  }
  function selectTopic(value: string) {
    setParams(value === 'all' ? {} : { topic: value }, { replace: true });
    setPage(1);
  }
  if (queue)
    return (
      <VocabularySession
        queue={queue}
        onBack={() => {
          stopSpeech();
          setQueue(undefined);
        }}
      />
    );
  return (
    <div className="lexicon">
      <header className="page-title">
        <div>
          <h1>
            {t('vocabulary')} · {languageNames[language][settings.language]}
          </h1>
        </div>
        <button className="primary" disabled={!filtered.length} onClick={() => start()}>
          {bi('Luyện 10 từ', 'Practice 10 words')}
        </button>
      </header>
      <div className="stats">
        <div className="stat">
          <span>{bi('Từ trong thư viện', 'Words in library')}</span>
          <strong>{words.length.toLocaleString(locale)}</strong>
        </div>
        <div className="stat">
          <span>{bi('Chủ đề', 'Topics')}</span>
          <strong>{vocabularyTopics.length}</strong>
        </div>
        <div className="stat">
          <span>{bi('Từ đã luyện', 'Words practised')}</span>
          <strong>{learned}</strong>
        </div>
      </div>
      <section aria-label={bi('Chọn chủ đề', 'Choose a topic')}>
        <div className="lexicon-section-heading">
          <h2>{bi('Bạn muốn khám phá gì?', 'What will you explore?')}</h2>
          <span className="muted">
            {bi('Chọn một chủ đề để bắt đầu', 'Find a topic that interests you')}
          </span>
        </div>
        <div className="lexicon-topics">
          <button
            className="lexicon-topic"
            aria-pressed={topic === 'all'}
            onClick={() => selectTopic('all')}
          >
            {t('allTopics')} <small>{words.length}</small>
          </button>
          {vocabularyTopics.map((item) => (
            <button
              key={item.id}
              className="lexicon-topic"
              data-topic={item.id}
              aria-pressed={topic === item.id}
              onClick={() => selectTopic(item.id)}
            >
              <span aria-hidden="true">{item.mark}</span> {item[locale]}{' '}
              <small>{words.filter((word) => word.topic === item.id).length}</small>
            </button>
          ))}
        </div>
      </section>
      <div className="lexicon-toolbar">
        <label className="lexicon-search">
          {bi('Tìm từ vựng', 'Search vocabulary')}
          <input
            type="search"
            value={search}
            onChange={(event) => {
              setSearch(event.target.value);
              setPage(1);
            }}
            placeholder={
              language === 'ja'
                ? bi('Chữ Nhật, kana, romaji hoặc nghĩa…', 'Japanese, kana, romaji or meaning…')
                : bi('Chữ Trung, pinyin hoặc nghĩa…', 'Chinese, pinyin or meaning…')
            }
          />
        </label>
        <p className="muted">{bi('Gõ không dấu để tìm nhanh', 'Search with or without accents')}</p>
      </div>
      <div className="lexicon-section-heading">
        <h2 ref={resultHeading} tabIndex={-1}>
          {topic === 'all'
            ? bi('Thư viện từ vựng', 'Word library')
            : vocabularyTopics.find((item) => item.id === topic)![locale]}
        </h2>
        <p role="status">
          {filtered.length.toLocaleString(locale)} {bi('kết quả', 'results')}
        </p>
      </div>
      {error && <Notice error>{error}</Notice>}
      {audioError && (
        <Notice>
          {bi(
            'Chưa phát được âm thanh. Hãy kiểm tra giọng đọc tiếng Nhật/Trung của trình duyệt.',
            'Audio is unavailable. Check your browser’s Japanese/Chinese voices.',
          )}
        </Notice>
      )}
      {displayed.length ? (
        <div className="lexicon-grid">
          {displayed.map((word) => (
            <article className="lexicon-card" key={word.id} data-topic={word.topic}>
              <div className="lexicon-card-top">
                <span>{vocabularyTopics.find((item) => item.id === word.topic)![locale]}</span>
                <button onClick={() => listen(word)} aria-label={`${t('listen')}: ${word.text}`}>
                  <SkillIcon skill="speaker" size={18} />
                </button>
              </div>
              <h3 className="lexicon-script" lang={language}>
                {word.text}
              </h3>
              <p className="lexicon-reading" lang={language === 'ja' ? 'ja' : 'zh-Latn'}>
                {word.reading}
              </p>
              {language === 'ja' && (
                <p className="lexicon-romanization" lang="ja-Latn">
                  {word.romanization}
                </p>
              )}
              <p className="lexicon-meaning">{word.meaning[locale]}</p>
              <div className="lexicon-card-footer">
                <small>
                  {practiced.has(word.text)
                    ? bi('Đã luyện', 'Practiced')
                    : bi('Từ mới', 'New word')}
                </small>
                <button
                  onClick={() => start(word)}
                  aria-label={`${bi('Học từ', 'Learn word')}: ${word.text}`}
                >
                  {bi('Học từ này', 'Learn this word')} <span aria-hidden="true">→</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <section className="lexicon-empty">
          <h3>{bi('Chưa tìm thấy từ phù hợp', 'No matching words')}</h3>
          <p>
            {bi(
              'Thử cách viết khác hoặc chọn tất cả chủ đề.',
              'Try a different spelling or choose all topics.',
            )}
          </p>
          <button
            onClick={() => {
              setSearch('');
              selectTopic('all');
            }}
          >
            {bi('Xóa tìm kiếm và bộ lọc', 'Clear search and filters')}
          </button>
        </section>
      )}
      {filtered.length > PAGE_SIZE && (
        <nav
          className="lexicon-pagination"
          aria-label={bi('Phân trang từ vựng', 'Vocabulary pagination')}
        >
          <button
            disabled={currentPage <= 1}
            onClick={() => {
              setPage(currentPage - 1);
              resultHeading.current?.focus();
            }}
          >
            {bi('← Trang trước', '← Previous page')}
          </button>
          <label>
            {bi('Trang', 'Page')}{' '}
            <select
              aria-label={bi('Chọn trang', 'Choose page')}
              value={currentPage}
              onChange={(event) => {
                setPage(Number(event.target.value));
                resultHeading.current?.focus();
              }}
            >
              {Array.from({ length: pages }, (_, i) => (
                <option key={i + 1} value={i + 1}>
                  {i + 1} / {pages}
                </option>
              ))}
            </select>
          </label>
          <button
            disabled={currentPage >= pages}
            onClick={() => {
              setPage(currentPage + 1);
              resultHeading.current?.focus();
            }}
          >
            {bi('Trang sau →', 'Next page →')}
          </button>
        </nav>
      )}
    </div>
  );
}

function VocabularySession({ queue, onBack }: { queue: WordQuestion[]; onBack: () => void }) {
  const bi = useBi();
  const t = useT();
  const settings = useApp((s) => s.settings);
  const [index, setIndex] = useState(0);
  const [choice, setChoice] = useState('');
  const [saved, setSaved] = useState(false);
  const [correct, setCorrect] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [audioError, setAudioError] = useState(false);
  const saving = useRef(false);
  const started = useRef(Date.now());
  const heading = useRef<HTMLHeadingElement>(null);
  const card = queue[index];
  const completed = index >= queue.length;
  useEffect(() => {
    heading.current?.focus();
  }, [index]);
  useEffect(() => () => stopSpeech(), []);
  async function submit() {
    if (!card || !choice || saved || saving.current) return;
    saving.current = true;
    setBusy(true);
    setError(false);
    try {
      const passed = choice === card.word.id;
      await saveWordPractice(card.word, passed, started.current);
      setSaved(true);
      setCorrect((value) => value + Number(passed));
    } catch {
      setError(true);
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }
  function next() {
    stopSpeech();
    setIndex((value) => value + 1);
    setChoice('');
    setSaved(false);
    setAudioError(false);
    started.current = Date.now();
  }
  return (
    <section className="lexicon-practice">
      <div className="lexicon-section-heading">
        <button disabled={busy} onClick={onBack}>
          {bi('← Về thư viện', '← Back to library')}
        </button>
        <span>{bi('Kết quả đã lưu được giữ lại', 'Saved results are kept')}</span>
      </div>
      {completed ? (
        <div className="lexicon-session-result panel">
          <span aria-hidden="true">✦</span>
          <h1 ref={heading} tabIndex={-1}>
            {t('result')}
          </h1>
          <p>
            {bi(
              `Bạn trả lời đúng ${correct}/${queue.length} từ.`,
              `You answered ${correct}/${queue.length} words correctly.`,
            )}
          </p>
          <p>
            {bi(
              'Một chút mỗi ngày, thêm tự tin mỗi lần.',
              'A little practice, a little more confidence.',
            )}
          </p>
          <button className="primary" onClick={onBack}>
            {bi('Tiếp tục khám phá', 'Keep exploring')} →
          </button>
        </div>
      ) : (
        <>
          <div className="lexicon-section-heading">
            <h1 ref={heading} tabIndex={-1}>
              {bi('Ghi nhớ từng từ', 'One word at a time')}
            </h1>
            <span>
              {index + 1} / {queue.length}
            </span>
          </div>
          <progress value={index + Number(saved)} max={queue.length} aria-label={t('progress')} />
          <div className="lexicon-practice-card panel" data-topic={card.word.topic}>
            <p className="lexicon-eyebrow">
              {vocabularyTopics.find((item) => item.id === card.word.topic)![settings.language]}
            </p>
            <p className="lexicon-script" lang={card.word.language}>
              {card.word.text}
            </p>
            <p className="lexicon-reading" lang={card.word.language === 'ja' ? 'ja' : 'zh-Latn'}>
              {card.word.reading}
            </p>
            {card.word.language === 'ja' && (
              <p className="lexicon-romanization" lang="ja-Latn">
                {card.word.romanization}
              </p>
            )}
            <button
              onClick={() => {
                setAudioError(false);
                if (
                  !speak(
                    card.word.text,
                    {
                      accent: card.word.language === 'ja' ? 'ja-JP' : 'zh-CN',
                      rate: settings.rate,
                    },
                    0,
                    () => setAudioError(true),
                  )
                )
                  setAudioError(true);
              }}
            >
              <SkillIcon skill="speaker" size={18} />
              {t('listen')}
            </button>
            {audioError && (
              <Notice>
                {bi(
                  'Giọng đọc chưa khả dụng trong trình duyệt này.',
                  'A suitable voice is unavailable in this browser.',
                )}
              </Notice>
            )}
            <fieldset disabled={saved || busy}>
              <legend>{bi('Từ này có nghĩa là gì?', 'What does this word mean?')}</legend>
              {card.options.map((option) => (
                <label className="lexicon-answer" key={option.id}>
                  <input
                    type="radio"
                    name="word-meaning"
                    checked={choice === option.id}
                    onChange={() => setChoice(option.id)}
                  />
                  <span>{option.meaning[settings.language]}</span>
                </label>
              ))}
            </fieldset>
            {error && (
              <Notice error>
                {bi(
                  'Không lưu được kết quả. Hãy thử lại.',
                  'Could not save your result. Please retry.',
                )}
              </Notice>
            )}
            {saved ? (
              <>
                <Notice>
                  {choice === card.word.id
                    ? bi('Chính xác!', 'Correct!')
                    : bi('Hãy ghi nhớ nghĩa này:', 'Remember this meaning:')}{' '}
                  {card.word.meaning[settings.language]} · {bi('Đã lưu kết quả', 'Result saved')}
                </Notice>
                <button className="primary" onClick={next}>
                  {index + 1 === queue.length
                    ? bi('Xem kết quả', 'View results')
                    : bi('Tiếp tục', 'Continue')}{' '}
                  →
                </button>
              </>
            ) : (
              <button className="primary" disabled={!choice || busy} onClick={() => void submit()}>
                {busy ? t('loading') : bi('Kiểm tra & lưu', 'Check & save')}
              </button>
            )}
          </div>
        </>
      )}
    </section>
  );
}
