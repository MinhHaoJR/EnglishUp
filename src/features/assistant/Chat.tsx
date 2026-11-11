import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { ApiError, useAuth } from '../../services/auth';
import {
  ask,
  fetchConversation,
  MAX_QUESTION_LENGTH,
  sourcePath,
  type ChatMessage,
} from '../../services/assistant';

const sourceLabel = {
  word: ['Từ vựng', 'Vocabulary'],
  reading: ['Bài đọc', 'Reading'],
  listening: ['Bài nghe', 'Listening'],
  writing: ['Đề viết', 'Writing task'],
  grammar: ['Cấu trúc câu', 'Sentence pattern'],
  guide: ['Hướng dẫn EnglishUp', 'EnglishUp guide'],
  roadmap: ['Lộ trình học', 'Learning path'],
} as Record<string, [string, string]>;
/** Each source wears its skill line, like the lessons it links to. */
export const sourceSkill: Record<string, IconName> = {
  word: 'vocabulary',
  reading: 'reading',
  listening: 'listening',
  writing: 'writing',
  grammar: 'grammar',
  guide: 'assistant',
  roadmap: 'roadmap',
};

const suggestions: [IconName, string, string][] = [
  [
    'reading',
    '"routine" và "habit" khác nhau thế nào?',
    'How are "routine" and "habit" different?',
  ],
  ['assistant', 'Mai muốn mua quà sinh nhật cho ai?', 'Who is Mai buying a birthday gift for?'],
  ['mail', 'Làm sao viết email mời bạn đi chơi?', 'How do I write an email inviting a friend out?'],
];
export const asset = (name: string) => `/tutor/${name}`;

/** One conversation with the tutor; shared by the full page and the floating mini chat. */
export function useChat(onAsked?: () => void) {
  const email = useAuth((state) => state.email);
  const [current, setCurrent] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<number | null>(null);
  const [left, setLeft] = useState<number | null>(null);
  const fail = (e: unknown) => setError(e instanceof ApiError ? e.status : 0);

  function startNew() {
    setCurrent(null);
    setMessages([]);
    setError(null);
  }

  // A different learner must not see the previous learner's chat.
  useEffect(() => {
    setCurrent(null);
    setMessages([]);
    setError(null);
    setLeft(null);
  }, [email]);

  async function open(id: string) {
    setError(null);
    try {
      setMessages(await fetchConversation(id));
      setCurrent(id);
    } catch (e) {
      fail(e);
    }
  }

  async function submit(text = question.trim()) {
    if (!text || busy) return;
    setBusy(true);
    setError(null);
    setQuestion(text);
    const now = new Date().toISOString();
    setMessages((list) => [
      ...list,
      { role: 'user', content: text, createdAt: now, citations: [] },
    ]);
    try {
      const reply = await ask(text, current);
      setMessages((list) => [
        ...list,
        { role: 'assistant', content: reply.answer, createdAt: now, citations: reply.citations },
      ]);
      setCurrent(reply.conversationId);
      setLeft(reply.questionsLeft);
      setQuestion('');
      onAsked?.();
    } catch (e) {
      // The question was not saved on the server, so take it back out of the log and keep it in the box.
      setMessages((list) => list.slice(0, -1));
      fail(e);
    } finally {
      setBusy(false);
    }
  }

  return {
    current,
    messages,
    question,
    setQuestion,
    busy,
    error,
    left,
    submit,
    open,
    startNew,
    fail,
  };
}

/** Tom, the tutor: a cartoon kitten in a mortarboard, from the app owner's own artwork. */
export function TutorAvatar({ size = 28 }: { size?: number }) {
  return (
    <img
      className="tutor-avatar"
      src={asset('tom-avatar.webp')}
      width={size}
      height={size}
      alt=""
      draggable={false}
    />
  );
}

/** Small drawn decorations around Tom: a four-point sparkle and a paw print. */
export function Sparkle({ className }: { className: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z" />
    </svg>
  );
}
export function Paw({ className }: { className: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <ellipse cx="12" cy="16" rx="5" ry="4.2" />
      <ellipse cx="5.5" cy="10.5" rx="2" ry="2.6" />
      <ellipse cx="9.5" cy="6.5" rx="2" ry="2.7" />
      <ellipse cx="14.5" cy="6.5" rx="2" ry="2.7" />
      <ellipse cx="18.5" cy="10.5" rx="2" ry="2.6" />
    </svg>
  );
}

const icons = {
  send: 'M4 12l16-8-6 16-2.5-6.5z M11.5 13.5L20 4',
  compose: 'M4 20h4L19 9l-4-4L4 16z M14 6l4 4',
  expand: 'M14 4h6v6 M20 4l-7 7 M10 20H4v-6 M4 20l7-7',
  minimize: 'M5 12h14',
  close: 'M6 6l12 12 M18 6L6 18',
} as const;

export function IconButton({
  icon,
  label,
  onClick,
  ...rest
}: { icon: keyof typeof icons; label: string } & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      className="icon-button"
      aria-label={label}
      title={label}
      onClick={onClick}
      {...rest}
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        aria-hidden="true"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d={icons[icon]} />
      </svg>
    </button>
  );
}

/** Messenger-style frame: avatar, name and status on top, the conversation below. */
export function ChatWindow({
  busy = false,
  actions,
  children,
}: {
  busy?: boolean;
  actions?: React.ReactNode;
  children: React.ReactNode;
}) {
  const bi = useBi();
  return (
    <div className="chat-window">
      <header className="chat-header">
        <span className="chat-header-avatar">
          <TutorAvatar size={48} />
          <span className={busy ? 'chat-presence busy' : 'chat-presence'} aria-hidden="true" />
        </span>
        <div className="chat-header-text">
          <strong>{bi('Trợ giảng Tom', 'Tutor Tom')}</strong>
          <small>
            <span className={busy ? 'chat-presence busy' : 'chat-presence'} aria-hidden="true" />
            {busy
              ? bi('Đang soạn câu trả lời…', 'Typing an answer…')
              : bi('Luôn sẵn sàng', 'Always here')}
          </small>
        </div>
        <div className="chat-header-actions">{actions}</div>
      </header>
      {children}
    </div>
  );
}

export function SignInNotice() {
  const bi = useBi();
  const { pathname } = useLocation();
  return (
    <Notice>
      {bi('Trợ giảng chạy trên máy chủ. Hãy', 'The tutor runs on the server. Please')}{' '}
      <Link to={`/login?next=${pathname}`}>
        {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
      </Link>{' '}
      {bi('để hỏi.', 'to ask.')}
    </Notice>
  );
}

/** Answers come as paragraphs; each becomes its own bubble, like a run of chat messages. */
const bubbles = (text: string) =>
  text
    .split(/\n\s*\n/)
    .map((part) => part.trim())
    .filter(Boolean);

/** Scrolling conversation, typing indicator, errors and the message box. */
export function ChatPanel({
  chat,
  autoFocus = false,
  intro,
  footnote,
}: {
  chat: ReturnType<typeof useChat>;
  autoFocus?: boolean;
  /** Replaces the mini chat's greeting (the full page has its own empty state). */
  intro?: React.ReactNode;
  /** Replaces the line under the message box. */
  footnote?: React.ReactNode;
}) {
  const bi = useBi();
  const scroller = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLTextAreaElement>(null);
  const { messages, busy, error, left, question } = chat;

  useEffect(() => {
    if (autoFocus) input.current?.focus();
  }, [autoFocus]);

  // Follow the newest message; an empty chat stays at the top, where Tom and the suggestions are.
  useEffect(() => {
    if (!messages.length && !busy && error === null) return;
    scroller.current?.scrollTo?.({ top: scroller.current.scrollHeight });
  }, [messages.length, busy, error]);

  // Grow the box with its text, back to one line once sent.
  useEffect(() => {
    const box = input.current;
    if (!box) return;
    box.style.height = 'auto';
    if (question) box.style.height = `${box.scrollHeight}px`;
  }, [question]);

  const errorText =
    error === 429
      ? bi(
          'Bạn đã dùng hết số câu hỏi hôm nay. Trợ giảng mở lại lúc 0 giờ.',
          'You have used all of today’s questions. The tutor resets at midnight.',
        )
      : error === 503
        ? bi(
            'Trợ giảng tạm thời không trả lời được vì hết hạn mức AI miễn phí. Hãy thử lại sau.',
            'The tutor cannot answer right now because the free AI quota is used up. Try again later.',
          )
        : bi(
            'Không kết nối được trợ giảng. Hãy kiểm tra mạng rồi thử lại.',
            'Cannot reach the tutor. Check your connection and try again.',
          );

  return (
    <>
      <div className="chat-scroll" ref={scroller}>
        {/* Once the learner asks, the welcome steps aside and only the conversation remains. */}
        {intro !== undefined ? (
          intro
        ) : messages.length === 0 && !busy ? (
          <div className="chat-intro">
            <div className="tom-stage">
              <Sparkle className="tom-star one" />
              <Sparkle className="tom-star two" />
              <Paw className="tom-paw" />
              <img src={asset('tom-hero.webp')} width={248} height={167} alt="" draggable={false} />
            </div>
            <div className="chat-intro-card">
              <strong>{bi('Trợ giảng Tom', 'Tutor Tom')}</strong>
              <p>
                {bi(
                  'Hỏi mình về từ vựng, bài đọc, bài nghe và đề viết trong EnglishUp. Mình chỉ trả lời từ bài học của app và ghi rõ nguồn.',
                  "Ask me about EnglishUp's vocabulary, readings, listening scripts and writing tasks. I answer only from the app's lessons and cite them.",
                )}
              </p>
            </div>
            <p className="chat-privacy">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M9 18h6 M10 21h4 M12 3a6 6 0 0 0-3.5 10.9c.6.4 1 1.1 1 1.8V16h5v-.3c0-.7.4-1.4 1-1.8A6 6 0 0 0 12 3z" />
              </svg>
              {bi(
                'Câu hỏi được gửi tới Google Gemini (gói miễn phí, Google có thể dùng để cải thiện dịch vụ). Đừng nhập thông tin cá nhân.',
                'Questions are sent to Google Gemini (free tier; Google may use them to improve its services). Do not enter personal information.',
              )}
            </p>
            <div className="chat-suggestions">
              {suggestions.map(([icon, vi, en]) => (
                <button key={en} type="button" onClick={() => void chat.submit(bi(vi, en))}>
                  <SkillIcon skill={icon} size={20} />
                  <span>{bi(vi, en)}</span>
                  <SkillIcon skill="chevron" size={18} />
                </button>
              ))}
            </div>
          </div>
        ) : null}
        <ol className="chat-log" aria-live="polite">
          {messages.map((m, i) => (
            <li key={i} className={`chat-row ${m.role}`}>
              <span className="sr-only">
                {m.role === 'user' ? bi('Bạn:', 'You:') : bi('Trợ giảng:', 'Tutor:')}
              </span>
              {m.role === 'assistant' && <TutorAvatar />}
              <div className="chat-stack">
                {bubbles(m.content).map((part, j) => (
                  <p key={j} className="bubble">
                    {part}
                  </p>
                ))}
              </div>
              {/* Wraps onto its own line, so the avatar stays beside the last bubble. */}
              {m.citations.length > 0 && (
                <ul className="citations" aria-label={bi('Nguồn', 'Sources')}>
                  {m.citations.map((c) => (
                    <li key={c.n} data-skill={sourceSkill[c.sourceType]}>
                      <span className="citation-n">{c.n}</span>
                      <span className="citation-tile" aria-hidden="true">
                        <SkillIcon skill={sourceSkill[c.sourceType] ?? 'reading'} size={14} />
                      </span>
                      <Link to={sourcePath(c.sourceType)}>
                        {bi(...(sourceLabel[c.sourceType] ?? ['Bài học', 'Lesson']))}: {c.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
          {busy && (
            <li className="chat-row assistant">
              <TutorAvatar />
              <div className="chat-stack">
                <p className="bubble typing">
                  <span className="sr-only">
                    {bi('Đang tìm trong bài học…', 'Searching the lessons…')}
                  </span>
                  <i aria-hidden="true" />
                  <i aria-hidden="true" />
                  <i aria-hidden="true" />
                </p>
              </div>
            </li>
          )}
        </ol>
        {error !== null && <Notice error>{errorText}</Notice>}
      </div>
      <form
        className="chat-composer"
        onSubmit={(e) => {
          e.preventDefault();
          void chat.submit();
        }}
      >
        <div className="chat-input">
          <Sparkle className="chat-input-icon" />
          <textarea
            ref={input}
            aria-label={bi('Câu hỏi của bạn', 'Your question')}
            value={question}
            maxLength={MAX_QUESTION_LENGTH}
            rows={1}
            onChange={(e) => chat.setQuestion(e.target.value)}
            onKeyDown={(e) => {
              // Enter sends, Shift+Enter starts a new line, as in most chat apps.
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
                e.preventDefault();
                e.currentTarget.form?.requestSubmit();
              }
            }}
            placeholder={bi('Nhắn cho trợ giảng Tom…', 'Message Tutor Tom…')}
          />
        </div>
        <IconButton
          icon="send"
          label={bi('Gửi', 'Send')}
          type="submit"
          disabled={busy || !question.trim()}
        />
      </form>
      <p className="chat-footnote">
        {footnote ?? (
          <>
            {left !== null && (
              <>
                <span>{bi(`Còn ${left} câu hỏi hôm nay`, `${left} questions left today`)}</span>{' '}
                ·{' '}
              </>
            )}
            <SkillIcon skill="shield" size={14} />{' '}
            {bi(
              'Trợ giảng có thể sai, hãy kiểm tra nguồn.',
              'The tutor can be wrong; check the sources.',
            )}
          </>
        )}
      </p>
    </>
  );
}
