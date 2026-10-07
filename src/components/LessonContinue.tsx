import { useBi } from '../i18n';

export function LessonContinue({
  onContinue,
  hasNext,
}: {
  onContinue: () => void;
  hasNext: boolean;
}) {
  const bi = useBi();
  return (
    <div className="actions mt-5">
      <button className="primary" onClick={onContinue}>
        {hasNext ? bi('Tiếp tục', 'Continue') : bi('Về danh sách bài học', 'Back to lessons')} →
      </button>
    </div>
  );
}
