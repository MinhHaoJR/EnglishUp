import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useBi } from '../../i18n';
import { Notice, PageTitle } from '../../components/shared';
import { ApiError, useAuth } from '../../services/auth';
import {
  ask,
  deleteConversation,
  fetchConversation,
  fetchConversations,
  MAX_QUESTION_LENGTH,
  sourcePath,
  type ChatMessage,
  type ConversationSummary,
} from '../../services/assistant';

const sourceLabel = {
  word: ['Từ vựng', 'Vocabulary'],
  reading: ['Bài đọc', 'Reading'],
  listening: ['Bài nghe', 'Listening'],
  writing: ['Đề viết', 'Writing task'],
} as Record<string, [string, string]>;

export default function Assistant() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [current, setCurrent] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<number | null>(null);
  const [left, setLeft] = useState<number | null>(null);

  const reload = () =>
    fetchConversations()
      .then(setConversations)
      .catch(() => setConversations([]));

  useEffect(() => {
    if (email) void reload();
  }, [email]);

  async function open(id: string) {
    setError(null);
    try {
      setMessages(await fetchConversation(id));
      setCurrent(id);
    } catch (e) {
      setError(e instanceof ApiError ? e.status : 0);
    }
  }

  function startNew() {
    setCurrent(null);
    setMessages([]);
    setError(null);
  }

  async function remove(id: string) {
    try {
      await deleteConversation(id);
      if (current === id) startNew();
      await reload();
    } catch (e) {
      setError(e instanceof ApiError ? e.status : 0);
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
      void reload();
    } catch (e) {
      // The question was not saved on the server, so take it back out of the log and keep it in the box.
      setMessages((list) => list.slice(0, -1));
      setError(e instanceof ApiError ? e.status : 0);
    } finally {
      setBusy(false);
    }
  }

  const title = (
    <PageTitle
      title={bi('Trợ giảng AI', 'AI tutor')}
      description={bi(
        'Hỏi về từ vựng, bài đọc, bài nghe và đề viết trong EnglishUp. Trợ giảng chỉ trả lời từ bài học của app và ghi rõ nguồn.',
        "Ask about EnglishUp's vocabulary, readings, listening scripts and writing tasks. The tutor answers only from the app's lessons and cites them.",
      )}
    />
  );

  if (!email)
    return (
      <>
        {title}
        <Notice>
          {bi('Trợ giảng chạy trên máy chủ. Hãy', 'The tutor runs on the server. Please')}{' '}
          <Link to="/account">
            {bi('đăng nhập hoặc tạo tài khoản', 'sign in or create an account')}
          </Link>{' '}
          {bi('để hỏi.', 'to ask.')}
        </Notice>
      </>
    );

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
      {title}
      <div className="assistant-layout">
        <section className="panel" aria-labelledby="chat-list">
          <h2 id="chat-list">{bi('Cuộc trò chuyện', 'Conversations')}</h2>
          <button className="primary" onClick={startNew}>
            {bi('Cuộc trò chuyện mới', 'New conversation')}
          </button>
          {conversations.length ? (
            <ul className="chat-list">
              {conversations.map((c) => (
                <li key={c.id}>
                  <button
                    aria-current={c.id === current || undefined}
                    onClick={() => void open(c.id)}
                  >
                    {c.title || bi('(không có tiêu đề)', '(untitled)')}
                  </button>
                  <button
                    aria-label={`${bi('Xoá', 'Delete')}: ${c.title}`}
                    onClick={() => void remove(c.id)}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">{bi('Chưa có cuộc trò chuyện nào.', 'No conversations yet.')}</p>
          )}
        </section>
        <section className="panel" aria-labelledby="chat-current">
          <h2 id="chat-current">
            {current ? bi('Trò chuyện', 'Chat') : bi('Câu hỏi mới', 'New question')}
          </h2>
          <ol className="chat-log" aria-live="polite">
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
          <form onSubmit={(e) => void send(e)} className="space-y-4">
            <label>
              {bi('Câu hỏi của bạn', 'Your question')}
              <textarea
                value={question}
                maxLength={MAX_QUESTION_LENGTH}
                rows={3}
                onChange={(e) => setQuestion(e.target.value)}
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
          <p className="muted">
            {bi(
              'Câu hỏi được gửi tới Google Gemini (gói miễn phí, Google có thể dùng để cải thiện dịch vụ). Đừng nhập thông tin cá nhân. Câu trả lời có thể sai; hãy kiểm tra nguồn.',
              'Questions are sent to Google Gemini (free tier; Google may use them to improve its services). Do not enter personal information. Answers can be wrong; check the sources.',
            )}
          </p>
        </section>
      </div>
    </>
  );
}
