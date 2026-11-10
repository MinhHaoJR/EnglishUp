/** One line-drawn pictogram set (24px grid, 1.8 stroke), used for the nav, skill lines and status signs. */
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
  grammar: 'M5 4h14v16H5z M8 8h3 M13 8h3 M8 12h8 M8 16h5',
  game: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7v5l3 2 M9 1h6',
  achievements:
    'M8 4h8v5a4 4 0 0 1-8 0V4z M8 6H5a3 3 0 0 0 3 4 M16 6h3a3 3 0 0 1-3 4 M12 13v4 M8 21h8 M10 17h4',
  streak: 'M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-4 3-5 0 2 1 3 2 3 0-3-1-5 0-8z',
  goal: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z M12 11v2',
  check: 'M5 12.5l4.5 4.5L19 7',
  arrow: 'M5 12h14 M13 6l6 6-6 6',
  speaker: 'M4 9h4l5-4v14l-5-4H4z M16.5 9a4 4 0 0 1 0 6 M19 6.5a7.5 7.5 0 0 1 0 11',
  play: 'M7 5v14l11-7z',
  stop: 'M6 6h12v12H6z',
  download: 'M12 4v11 M7 10l5 5 5-5 M5 20h14',
  upload: 'M12 20V9 M7 14l5-5 5 5 M5 4h14',
  cards: 'M8 4h10a2 2 0 0 1 2 2v10 M4 8h11a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8z',
  choice: 'M4 6.5h2 M9 6.5h11 M4 12h2 M9 12h11 M4 17.5h2 M9 17.5h11',
  keyboard: 'M3 6h18v12H3z M7 10h1 M11 10h2 M16 10h1 M7 14h10',
  sync: 'M20 11a8 8 0 0 0-14.5-4.5 M4 3v4h4 M4 13a8 8 0 0 0 14.5 4.5 M20 21v-4h-4',
  eye: 'M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  eyeOff:
    'M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z M4 4l16 16',
} as const;

export type IconName = keyof typeof paths;

export default function SkillIcon({ skill, size = 20 }: { skill: IconName; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d={paths[skill]} />
    </svg>
  );
}
