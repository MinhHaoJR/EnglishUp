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
import { ChatPanel, IconButton, SignInNotice, TutorAvatar, useChat } from './Chat';

/*
THESIS: a contact sheet of conversations. Every saved chat is a small frame in the history rail;
only the open one is shown at full scale beside it. Refuses the boxed chat widget blown up to a page.
OWN-WORLD: the app's wayfinding signage (sign-blue, 12px plates, 1px rules, no shadows); answers read
as text with their sources labelled by skill line, questions stay as blue bubbles.
STORY: the learner asks or reopens a question, reads a cited answer, and follows a source to the lesson.
FIRST VIEWPORT: rail with New conversation and dated frames; the open frame fills the rest, composer
docked at its foot; an empty frame offers four questions, one per skill line.
FORM: structure #1 of 6 (workspace with history rail), "contact sheet" composition, seed 66dcd42e/0.
FINISH: critique pass in light, dark and 375px, then DESIGN.md.
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
      name: bi('Hôm nay', 'Today'),
      items: conversations.filter((c) => sameDay(new Date(c.updatedAt), now)),
    },
    {
      name: bi('Trước đó', 'Earlier'),
      items: conversations.filter((c) => !sameDay(new Date(c.updatedAt), now)),
    },
  ].filter((group) => group.items.length);
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
        <div className="tutor-rail-head">
          <h1>{bi('Trợ giảng Tom', 'Tutor Tom')}</h1>
          <button type="button" className="tutor-new" onClick={chat.startNew}>
            <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 5v14 M5 12h14" />
            </svg>
            {bi('Cuộc trò chuyện mới', 'New conversation')}
          </button>
        </div>
        {groups.length ? (
          groups.map((group) => (
            <section key={group.name} className="tutor-group">
              <h2>{group.name}</h2>
              <ul>
                {group.items.map((c) => (
                  <li key={c.id} className="tutor-frame">
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
      </nav>

      <section className="tutor-main" aria-labelledby="tutor-title">
        <header className="tutor-main-head">
          <TutorAvatar size={32} />
          <div>
            <h2 id="tutor-title">{open?.title ?? bi('Cuộc trò chuyện mới', 'New conversation')}</h2>
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
                  <h3>{bi('Hôm nay bạn muốn hỏi gì?', 'What would you like to ask today?')}</h3>
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
                          <small>{bi(...s.label)}</small>
                          {bi(...s.question)}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null
            }
            footnote={bi(
              'Trợ giảng có thể sai, hãy mở nguồn để kiểm tra. Câu hỏi được gửi tới Google Gemini (gói miễn phí); đừng nhập thông tin cá nhân.',
              'The tutor can be wrong; open the sources to check. Questions go to Google Gemini (free tier); do not enter personal information.',
            )}
          />
        </div>
      </section>
    </div>
  );
}
