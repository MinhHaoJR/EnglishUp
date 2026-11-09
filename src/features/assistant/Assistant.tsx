import { useEffect, useState } from 'react';
import { useBi } from '../../i18n';
import { PageTitle } from '../../components/shared';
import { useAuth } from '../../services/auth';
import {
  deleteConversation,
  fetchConversations,
  type ConversationSummary,
} from '../../services/assistant';
import { ChatPanel, SignInNotice, useChat } from './Chat';

/** Full tutor page: the same chat as the mini chat, plus the list of saved conversations. */
export default function Assistant() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const reload = () =>
    fetchConversations()
      .then(setConversations)
      .catch(() => setConversations([]));
  const chat = useChat(() => void reload());

  useEffect(() => {
    if (email) void reload();
  }, [email]);

  async function remove(id: string) {
    try {
      await deleteConversation(id);
      if (chat.current === id) chat.startNew();
      await reload();
    } catch (e) {
      chat.fail(e);
    }
  }

  const title = (
    <PageTitle
      title={bi('Trợ giảng AI', 'AI tutor')}
      description={bi(
        'Hỏi về từ vựng, bài đọc, bài nghe và đề viết trong EnglishUp. Trợ giảng chỉ trả lời từ bài học của app và ghi rõ nguồn. Bạn cũng có thể mở trợ giảng ở góc dưới bên phải của mọi trang.',
        "Ask about EnglishUp's vocabulary, readings, listening scripts and writing tasks. The tutor answers only from the app's lessons and cites them. You can also open it from the bottom-right corner of any page.",
      )}
    />
  );

  if (!email)
    return (
      <>
        {title}
        <SignInNotice />
      </>
    );

  return (
    <>
      {title}
      <div className="assistant-layout">
        <section className="panel" aria-labelledby="chat-list">
          <h2 id="chat-list">{bi('Cuộc trò chuyện', 'Conversations')}</h2>
          <button className="primary" onClick={chat.startNew}>
            {bi('Cuộc trò chuyện mới', 'New conversation')}
          </button>
          {conversations.length ? (
            <ul className="chat-list">
              {conversations.map((c) => (
                <li key={c.id}>
                  <button
                    aria-current={c.id === chat.current || undefined}
                    onClick={() => void chat.open(c.id)}
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
            {chat.current ? bi('Trò chuyện', 'Chat') : bi('Câu hỏi mới', 'New question')}
          </h2>
          <ChatPanel chat={chat} />
        </section>
      </div>
    </>
  );
}
