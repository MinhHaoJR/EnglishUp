import { useEffect, useState } from 'react';
import { useBi } from '../../i18n';
import { PageTitle } from '../../components/shared';
import SkillIcon, { type IconName } from '../../components/SkillIcon';
import { useApp } from '../../app/store';
import { useAuth } from '../../services/auth';
import {
  deleteConversation,
  fetchConversations,
  type ConversationSummary,
} from '../../services/assistant';
import {
  asset,
  ChatPanel,
  IconButton,
  Paw,
  SignInNotice,
  Sparkle,
  TutorAvatar,
  useChat,
} from './Chat';

/*
THESIS: Tutor Tom's room. Tom leans on the conversation card from a strip of sky, so the page reads as
talking to him, not filling a form. Follows the owner's reference image.
OWN-WORLD: soft sign-blue sky, 24px cards, round pill controls, skill-line tiles for the starters, a
faint London skyline under the history rail; answers read as text with cited sources.
STORY: the learner asks or reopens a question, reads a cited answer, and follows a source to the lesson.
FIRST VIEWPORT: rail (Tom card, New conversation, dated chats); sky with Tom, a speech bubble and his
name; below it the conversation card with four starters and the pill composer.
FINISH: checked in light, dark and 375px, then DESIGN.md.
*/

const starters: { skill: IconName; label: [string, string]; question: [string, string] }[] = [
  {
    skill: 'vocabulary',
    label: ['Từ vựng', 'Vocabulary'],
    question: [
      '"routine" và "habit" khác nhau thế nào?',
      'How are "routine" and "habit" different?',
    ],
  },
  {
    skill: 'reading',
    label: ['Bài đọc', 'Reading'],
    question: ['Vì sao Linh đổi thói quen buổi sáng?', 'Why did Linh change her morning routine?'],
  },
  {
    skill: 'writing',
    label: ['Viết', 'Writing'],
    question: [
      'Làm sao viết email mời bạn đi chơi?',
      'How do I write an email inviting a friend out?',
    ],
  },
  {
    skill: 'grammar',
    label: ['Cấu trúc câu', 'Sentence patterns'],
    question: ['Khi nào dùng "so ... that"?', 'When do I use "so ... that"?'],
  },
];

const sameDay = (a: Date, b: Date) => a.toDateString() === b.toDateString();

/** Full tutor page: saved conversations as a rail of frames, the open one at full size. */
export default function Assistant() {
  const bi = useBi();
  const locale = useApp((state) => (state.settings.language === 'vi' ? 'vi-VN' : 'en-US'));
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

  if (!email)
    return (
      <>
        <PageTitle
          title={bi('Trợ giảng Tom', 'Tutor Tom')}
          description={bi(
            'Trả lời từ bài học trong app, luôn kèm nguồn.',
            "Answers from the app's lessons, always with sources.",
          )}
        />
        <SignInNotice />
      </>
    );

  const now = new Date();
  const groups = [
    {
      icon: 'clock' as const,
      name: bi('Hôm nay', 'Today'),
      items: conversations.filter((c) => sameDay(new Date(c.updatedAt), now)),
    },
    {
      icon: 'history' as const,
      name: bi('Trước đó', 'Earlier'),
      items: conversations.filter((c) => !sameDay(new Date(c.updatedAt), now)),
    },
  ].filter((group) => group.items.length);
  const status = chat.busy
    ? bi('Đang soạn câu trả lời…', 'Typing an answer…')
    : bi('Luôn sẵn sàng', 'Always here');
  const when = (iso: string) => {
    const date = new Date(iso);
    return sameDay(date, now)
      ? date.toLocaleTimeString(locale, { hour: '2-digit', minute: '2-digit' })
      : date.toLocaleDateString(locale, { day: 'numeric', month: 'numeric' });
  };
  const open = conversations.find((c) => c.id === chat.current);
  const empty = chat.messages.length === 0 && !chat.busy;

  return (
    <div className="tutor">
      <nav className="tutor-rail" aria-label={bi('Lịch sử trò chuyện', 'Chat history')}>
        <div className="tutor-card">
          <span className="chat-header-avatar">
            <TutorAvatar size={52} />
            <span
              className={chat.busy ? 'chat-presence busy' : 'chat-presence'}
              aria-hidden="true"
            />
          </span>
          <div>
            <strong>{bi('Trợ giảng Tom', 'Tutor Tom')}</strong>
            <small>{status}</small>
          </div>
        </div>
        <button type="button" className="tutor-new" onClick={chat.startNew}>
          <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 5v14 M5 12h14" />
          </svg>
          {bi('Cuộc trò chuyện mới', 'New conversation')}
        </button>
        <div className="tutor-history">
          {groups.length ? (
            groups.map((group) => (
              <section key={group.name} className="tutor-group">
                <h2>
                  <SkillIcon skill={group.icon} size={18} />
                  {group.name}
                </h2>
                <ul>
                  {group.items.map((c) => (
                    <li key={c.id} className="tutor-frame">
                      <span className="tutor-frame-icon" aria-hidden="true">
                        <SkillIcon skill="assistant" size={16} />
                      </span>
                      <button
                        type="button"
                        aria-current={c.id === chat.current || undefined}
                        onClick={() => void chat.open(c.id)}
                      >
                        {c.title || bi('(không có tiêu đề)', '(untitled)')}
                      </button>
                      <time dateTime={c.updatedAt}>{when(c.updatedAt)}</time>
                      <IconButton
                        icon="close"
                        label={`${bi('Xoá', 'Delete')}: ${c.title}`}
                        onClick={() => void remove(c.id)}
                      />
                    </li>
                  ))}
                </ul>
              </section>
            ))
          ) : (
            <p className="tutor-rail-empty">
              {bi('Chưa có cuộc trò chuyện nào.', 'No conversations yet.')}
            </p>
          )}
        </div>
        <span className="tutor-skyline" aria-hidden="true" />
      </nav>

      <div className="tutor-stage">
        <header className="tutor-sky">
          <img
            className="tutor-peek"
            src={asset('tom-peek.webp')}
            width={320}
            height={226}
            alt=""
            draggable={false}
          />
          <p className="tutor-bubble" aria-hidden="true">
            <span>{bi('Học tiếng Anh', 'English made')}</span>
            <span>
              {bi('thật dễ dàng!', 'easy!')}
              <svg viewBox="0 0 24 24">
                <path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" />
              </svg>
            </span>
          </p>
          <div className="tutor-sky-title">
            <h1>{bi('Trợ giảng Tom', 'Tutor Tom')}</h1>
            <p>
              <span
                className={chat.busy ? 'chat-presence busy' : 'chat-presence'}
                aria-hidden="true"
              />
              {status}
            </p>
          </div>
          <Paw className="tutor-sky-paw one" />
          <Paw className="tutor-sky-paw two" />
          <Paw className="tutor-sky-paw three" />
        </header>

        <section className="tutor-main" aria-labelledby="tutor-title">
          <header className="tutor-main-head">
            <span className="tutor-head-icon" aria-hidden="true">
              <SkillIcon skill={open ? 'assistant' : 'megaphone'} size={22} />
            </span>
            <div>
              <h2 id="tutor-title">
                {open?.title ?? bi('Cuộc trò chuyện mới', 'New conversation')}
              </h2>
              <small>
                {chat.busy
                  ? bi('Đang tìm trong bài học…', 'Searching the lessons…')
                  : bi(
                      'Trả lời từ bài học trong app, kèm nguồn',
                      "Answers from the app's lessons, with sources",
                    )}
              </small>
            </div>
            {chat.left !== null && (
              <span className="tutor-quota">
                {bi(`Còn ${chat.left} câu hỏi hôm nay`, `${chat.left} questions left today`)}
              </span>
            )}
          </header>
          <div className="tutor-thread">
            <ChatPanel
              chat={chat}
              intro={
                empty ? (
                  <div className="tutor-empty">
                    <h3>
                      <Sparkle className="tutor-empty-spark" />
                      {bi('Hôm nay bạn muốn hỏi gì?', 'What would you like to ask today?')}
                    </h3>
                    <p>
                      {bi(
                        'Hỏi về từ vựng, bài đọc, bài nghe, đề viết và cấu trúc câu trong EnglishUp. Mỗi ý trong câu trả lời đều ghi bài học làm nguồn.',
                        "Ask about EnglishUp's vocabulary, readings, listening, writing tasks and sentence patterns. Every point in an answer names its lesson.",
                      )}
                    </p>
                    <ul className="tutor-starters">
                      {starters.map((s) => (
                        <li key={s.skill} data-skill={s.skill}>
                          <button type="button" onClick={() => void chat.submit(bi(...s.question))}>
                            <span className="line-tile" aria-hidden="true">
                              <SkillIcon skill={s.skill} />
                            </span>
                            <strong>{bi(...s.label)}</strong>
                            <span>{bi(...s.question)}</span>
                            <SkillIcon skill="chevron" size={20} />
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null
              }
              footnote={
                <>
                  <SkillIcon skill="shield" size={16} />{' '}
                  {bi(
                    'Trợ giảng có thể sai, hãy kiểm tra nguồn. Câu hỏi được gửi tới Google Gemini (gói miễn phí); đừng nhập thông tin cá nhân.',
                    'The tutor can be wrong; check the sources. Questions go to Google Gemini (free tier); do not enter personal information.',
                  )}
                </>
              }
            />
          </div>
        </section>
      </div>
    </div>
  );
}
