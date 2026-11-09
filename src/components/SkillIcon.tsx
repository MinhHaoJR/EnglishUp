const paths = {
  dashboard: 'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
  vocabulary: 'M4 4h12a2 2 0 0 1 2 2v14H6a2 2 0 0 1-2-2V4z M4 16h14 M8 8h6 M21 7v14',
  listening: 'M4 14v-3a8 8 0 0 1 16 0v3 M4 12H3v7h4v-7H4z M20 12h1v7h-4v-7h3z',
  speaking: 'M9 5a3 3 0 0 1 6 0v6a3 3 0 0 1-6 0V5z M5 10v1a7 7 0 0 0 14 0v-1 M12 18v4 M8 22h8',
  reading:
    'M12 5C9 3 6 3 2 4v15c4-1 7-1 10 1 3-2 6-2 10-1V4c-4-1-7-1-10 1z M12 5v15 M5 8h4 M15 8h4',
  writing: 'm15 3 6 6 M4 15 16 3a2 2 0 0 1 3 0l2 2a2 2 0 0 1 0 3L9 20l-6 1z M4 15l5 5 M13 21h8',
  settings: 'M4 6h16 M4 12h16 M4 18h16 M8 3v6 M16 9v6 M10 15v6',
  assistant: 'M4 5h16v11H9l-5 4V5z M8 9h8 M8 12h5',
  game: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7v5l3 2 M9 1h6',
  achievements:
    'M8 4h8v5a4 4 0 0 1-8 0V4z M8 6H5a3 3 0 0 0 3 4 M16 6h3a3 3 0 0 1-3 4 M12 13v4 M8 21h8 M10 17h4',
} as const;

export default function SkillIcon({ skill }: { skill: keyof typeof paths }) {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d={paths[skill]} />
    </svg>
  );
}
