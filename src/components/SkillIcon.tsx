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
  admin: 'M12 3l8 3v6c0 4.8-3.4 8-8 9-4.6-1-8-4.2-8-9V6z M12 8v4 M12 15.5v.5',
  user: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M4 21a8 8 0 0 1 16 0',
  lock: 'M5 11h14v10H5z M8 11V7a4 4 0 0 1 8 0v4 M12 15v2',
  shield: 'M12 3l8 3v6c0 4.8-3.4 8-8 9-4.6-1-8-4.2-8-9V6z M9 12l2 2 4-4',
  logout: 'M14 4h5v16h-5 M10 8l-4 4 4 4 M6 12h10',
  chevron: 'M9 6l6 6-6 6',
  mail: 'M3 6h18v12H3z M3 7l9 6 9-6',
  gauge: 'M4 17a8 8 0 1 1 16 0 M12 17l4.5-5 M6.5 13l-1.2-.7 M12 9.5V8 M17.5 13l1.2-.7',
  sun: 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z M12 2v2 M12 20v2 M4.9 4.9l1.4 1.4 M17.7 17.7l1.4 1.4 M2 12h2 M20 12h2 M4.9 19.1l1.4-1.4 M17.7 6.3l1.4-1.4',
  moon: 'M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z',
  palette:
    'M12 3a9 9 0 1 0 0 18c1.2 0 2-.8 2-1.8 0-1.2-1-1.6-1-2.7 0-1 .8-1.5 1.8-1.5H17a4 4 0 0 0 4-4c0-4.4-4-8-9-8z M7.5 12h.5 M9.5 7.5h.5 M14.5 7.5h.5',
  trash: 'M4 7h16 M9 7V4h6v3 M6 7l1 13h10l1-13 M10 11v5 M14 11v5',
  clock: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7v5l3 2',
  history: 'M4.5 13a7.5 7.5 0 1 0 2.2-6.3 M4 3.5V8h4.5 M12 8v4.5l3 1.8',
  megaphone: 'M3 10v4h3l8 5V5l-8 5H3z M17.5 9a4 4 0 0 1 0 6 M6 14l1.5 5.5H10L9 14',
  globe:
    'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M3 12h18 M12 3c2.5 2.5 3.8 5.5 3.8 9s-1.3 6.5-3.8 9 M12 3c-2.5 2.5-3.8 5.5-3.8 9s1.3 6.5 3.8 9',
  roadmap:
    'M5 19a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M19 9a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M7 17h5a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h8',
  placement: 'M9 3h6v3H9z M7 5H5v16h14V5h-2 M8 12l2.5 2.5L16 9 M8 18h8',
  sync: 'M20 11a8 8 0 0 0-14.5-4.5 M4 3v4h4 M4 13a8 8 0 0 0 14.5 4.5 M20 21v-4h-4',
  eye: 'M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
  eyeOff:
    'M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z M4 4l16 16',
} as const;

export type IconName = keyof typeof paths;
export const isIconName = (name: string): name is IconName => name in paths;

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
