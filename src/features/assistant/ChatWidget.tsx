import { useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useBi } from '../../i18n';
import { useAuth } from '../../services/auth';
import { ChatPanel, ChatWindow, IconButton, SignInNotice, TutorAvatar, useChat } from './Chat';
import { useChatHead } from './chatHead';

/**
 * Chat head on every page, opening a messaging window beside it. It starts in the bottom-right corner
 * and the learner can drag it anywhere in the window. It lives in the app shell, so the conversation
 * survives moving between pages; the full /assistant page has its own.
 */
export default function ChatWidget() {
  const bi = useBi();
  const email = useAuth((state) => state.email);
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const chat = useChat();
  const toggle = useRef<HTMLButtonElement>(null);
  const place = useChatHead();

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
          style={place.panel}
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
        className={place.dragging ? 'chat-head dragging' : 'chat-head'}
        style={place.head}
        aria-label={label}
        aria-describedby="chat-head-hint"
        title={`${label} · ${bi('kéo để di chuyển', 'drag to move')}`}
        aria-expanded={open}
        aria-controls="chat-widget-panel"
        {...place.handlers}
        onClick={() => {
          if (place.clickWasDrag()) return;
          if (open) minimize();
          else setOpen(true);
        }}
      >
        <TutorAvatar size={56} />
        {chat.busy && <span className="chat-head-dot" aria-hidden="true" />}
      </button>
      <span id="chat-head-hint" className="sr-only">
        {bi(
          'Kéo, hoặc dùng các phím mũi tên, để đổi chỗ. Phím Home đưa về góc.',
          'Drag it, or use the arrow keys, to move it. Home puts it back in the corner.',
        )}
      </span>
    </div>
  );
}
