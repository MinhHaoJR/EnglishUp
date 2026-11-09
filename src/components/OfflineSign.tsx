import { useEffect, useState } from 'react';
import { useBi } from '../i18n';

/** A small status sign while the browser has no connection; lessons keep working underneath. */
export function OfflineSign() {
  const bi = useBi();
  const [online, setOnline] = useState(() => navigator.onLine);
  useEffect(() => {
    const update = () => setOnline(navigator.onLine);
    window.addEventListener('online', update);
    window.addEventListener('offline', update);
    return () => {
      window.removeEventListener('online', update);
      window.removeEventListener('offline', update);
    };
  }, []);
  if (online) return null;
  return (
    <p
      className="offline-sign"
      role="status"
      title={bi(
        'Bài học vẫn dùng được. Đồng bộ, trò chơi và trợ giảng sẽ chạy lại khi có mạng.',
        'Lessons still work. Sync, the race and the tutor return when you are back online.',
      )}
    >
      <span aria-hidden="true" />
      {bi('Đang offline', 'Offline')}
    </p>
  );
}
