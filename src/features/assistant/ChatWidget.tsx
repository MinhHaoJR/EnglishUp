import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useBi } from '../../i18n';
import { useAuth } from '../../services/auth';
import { ChatPanel, SignInNotice, useChat } from './Chat';

/**
 * Floating tutor in the bottom-right corner of every page. It lives in the app shell, so the
 * conversation survives moving between pages; the full /assistant page has its own copy.
 */
export default function ChatWidget() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const { pathname } = useLocation();
  const [open, setOpen] = useState(false);
  const chat = useChat();
  const input = useRef<HTMLTextAreaElement>(null);
  const toggle = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (open) input.current?.focus();
  }, [open]);

  function close() {
    setOpen(false);
    toggle.current?.focus();
  }

  if (pathname === '/assistant') return null;
  const label = bi('Trợ giảng AI', 'AI tutor');

  return (
    <div className="chat-widget">
      {open && (
        <section
          id="chat-widget-panel"
          className="chat-widget-panel"
          role="dialog"
          aria-label={label}
          onKeyDown={(e) => e.key === 'Escape' && close()}
        >
          <header>
            <strong>{label}</strong>
            {email && (
              <button onClick={chat.startNew} title={bi('Cuộc trò chuyện mới', 'New conversation')}>
                {bi('Mới', 'New')}
              </button>
            )}
            <Link to="/assistant" onClick={() => setOpen(false)}>
              {bi('Mở rộng', 'Full page')}
            </Link>
            <button aria-label={bi('Đóng trợ giảng', 'Close the tutor')} onClick={close}>
              ✕
            </button>
          </header>
          <div className="chat-widget-body">
            {email ? <ChatPanel chat={chat} inputRef={input} /> : <SignInNotice />}
          </div>
        </section>
      )}
      <button
        ref={toggle}
        className="chat-widget-toggle primary"
        aria-expanded={open}
        aria-controls="chat-widget-panel"
        onClick={() => (open ? close() : setOpen(true))}
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
          <path d="M4 5h16v11H9l-5 4V5z M8 9h8 M8 12h5" />
        </svg>
        {label}
      </button>
    </div>
  );
}
