import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice } from '../../components/shared';
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
} as Record<string, [string, string]>;

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

  async function send(event: React.FormEvent) {
    event.preventDefault();
    const text = question.trim();
    if (!text || busy) return;
    setBusy(true);
    setError(null);
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
    send,
    open,
    startNew,
    fail,
  };
}

export function SignInNotice() {
  const bi = useBi();
  return (
    <Notice>
      {bi('Trợ giảng chạy trên máy chủ. Hãy', 'The tutor runs on the server. Please')}{' '}
      <Link to="/account">
        {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
      </Link>{' '}
      {bi('để hỏi.', 'to ask.')}
    </Notice>
  );
}

/** Message log, question box, errors and the privacy note. */
export function ChatPanel({
  chat,
  inputRef,
}: {
  chat: ReturnType<typeof useChat>;
  inputRef?: React.Ref<HTMLTextAreaElement>;
}) {
  const bi = useBi();
  const log = useRef<HTMLOListElement>(null);
  const { messages, busy, error, left, question } = chat;

  useEffect(() => {
    log.current?.scrollTo?.({ top: log.current.scrollHeight });
  }, [messages.length, busy]);

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
      <ol className="chat-log" aria-live="polite" ref={log}>
        {messages.map((m, i) => (
          <li key={i} className={`chat-message ${m.role}`}>
            <strong>{m.role === 'user' ? bi('Bạn', 'You') : bi('Trợ giảng', 'Tutor')}</strong>
            <p>{m.content}</p>
            {m.citations.length > 0 && (
              <ul className="citations" aria-label={bi('Nguồn', 'Sources')}>
                {m.citations.map((c) => (
                  <li key={c.n}>
                    [{c.n}]{' '}
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
          <li className="chat-message assistant muted">
            {bi('Đang tìm trong bài học…', 'Searching the lessons…')}
          </li>
        )}
      </ol>
      <form onSubmit={(e) => void chat.send(e)} className="chat-form">
        <label>
          {bi('Câu hỏi của bạn', 'Your question')}
          <textarea
            ref={inputRef}
            value={question}
            maxLength={MAX_QUESTION_LENGTH}
            rows={3}
            onChange={(e) => chat.setQuestion(e.target.value)}
            onKeyDown={(e) => {
              // Enter sends, Shift+Enter starts a new line, as in most chat apps.
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
                e.preventDefault();
                e.currentTarget.form?.requestSubmit();
              }
            }}
            placeholder={bi(
              'Ví dụ: "routine" và "habit" khác nhau thế nào?',
              'For example: how are "routine" and "habit" different?',
            )}
          />
        </label>
        <div className="actions">
          <button className="primary" type="submit" disabled={busy || !question.trim()}>
            {bi('Gửi', 'Send')}
          </button>
          {left !== null && (
            <span className="muted">
              {bi(`Còn ${left} câu hỏi hôm nay`, `${left} questions left today`)}
            </span>
          )}
        </div>
      </form>
      {error !== null && <Notice error>{errorText}</Notice>}
      <p className="muted chat-note">
        {bi(
          'Câu hỏi được gửi tới Google Gemini (gói miễn phí, Google có thể dùng để cải thiện dịch vụ). Đừng nhập thông tin cá nhân. Câu trả lời có thể sai; hãy kiểm tra nguồn.',
          'Questions are sent to Google Gemini (free tier; Google may use them to improve its services). Do not enter personal information. Answers can be wrong; check the sources.',
        )}
      </p>
    </>
  );
}
