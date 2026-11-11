import { useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useBi } from '../../i18n';
import { useAuth } from '../../services/auth';
import { ChatPanel, ChatWindow, IconButton, SignInNotice, TutorAvatar, useChat } from './Chat';

/**
 * Chat head in the bottom-right corner of every page, opening a messaging window. It lives in the
 * app shell, so the conversation survives moving between pages; the full /assistant page has its own.
 */
export default function ChatWidget() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const chat = useChat();
  const toggle = useRef<HTMLButtonElement>(null);

  function minimize() {
    setOpen(false);
    toggle.current?.focus();
  }

  if (pathname === '/assistant') return null;
  const label = bi('Trợ giảng Tom', 'Tutor Tom');

  return (
    <div className="chat-widget">
      {open && (
        <section
          id="chat-widget-panel"
          className="chat-widget-panel"
          role="dialog"
          aria-label={label}
          onKeyDown={(e) => e.key === 'Escape' && minimize()}
        >
          <ChatWindow
            busy={chat.busy}
            actions={
              <>
                {email && (
                  <IconButton
                    icon="compose"
                    label={bi('Cuộc trò chuyện mới', 'New conversation')}
                    onClick={chat.startNew}
                  />
                )}
                <IconButton
                  icon="expand"
                  label={bi('Mở trang trợ giảng', 'Open the tutor page')}
                  onClick={() => {
                    setOpen(false);
                    navigate('/assistant');
                  }}
                />
                <IconButton icon="minimize" label={bi('Thu nhỏ', 'Minimize')} onClick={minimize} />
                <IconButton
                  icon="close"
                  label={bi('Đóng trợ giảng', 'Close the tutor')}
                  onClick={() => {
                    chat.startNew();
                    minimize();
                  }}
                />
              </>
            }
          >
            {email ? (
              <ChatPanel chat={chat} autoFocus />
            ) : (
              <div className="chat-scroll">
                <SignInNotice />
              </div>
            )}
          </ChatWindow>
        </section>
      )}
      <button
        ref={toggle}
        className="chat-head"
        aria-label={label}
        title={label}
        aria-expanded={open}
        aria-controls="chat-widget-panel"
        onClick={() => (open ? minimize() : setOpen(true))}
      >
        <TutorAvatar size={56} />
        {chat.busy && <span className="chat-head-dot" aria-hidden="true" />}
      </button>
    </div>
  );
}
