/** A five-point star on the flag grid, outer radius r, one point straight up. */
function star(cx: number, cy: number, r: number) {
  return Array.from({ length: 10 }, (_, i) => {
    const angle = ((i * 36 - 90) * Math.PI) / 180;
    const radius = i % 2 ? r * 0.382 : r;
    return `${(cx + radius * Math.cos(angle)).toFixed(2)},${(cy + radius * Math.sin(angle)).toFixed(2)}`;
  }).join(' ');
}

/** en is the British flag, us the American one; vi, ja and zh their countries. */
export type FlagCode = 'en' | 'us' | 'vi' | 'ja' | 'zh';

/** Small drawn flags on a 30 × 20 grid, simplified to read at 24px. */
export function Flag({ code }: { code: FlagCode }) {
  return (
    <svg className="language-flag" viewBox="0 0 30 20" aria-hidden="true">
      {code === 'en' && (
        <>
          <rect width="30" height="20" fill="#012169" />
          <path d="M0 0l30 20M30 0L0 20" stroke="#fff" strokeWidth="4" />
          <path d="M0 0l30 20M30 0L0 20" stroke="#c8102e" strokeWidth="1.5" />
          <path d="M15 0v20M0 10h30" stroke="#fff" strokeWidth="6" />
          <path d="M15 0v20M0 10h30" stroke="#c8102e" strokeWidth="3.4" />
        </>
      )}
      {code === 'us' && (
        <>
          <rect width="30" height="20" fill="#fff" />
          {[0, 2, 4, 6, 8, 10, 12].map((i) => (
            <rect key={i} y={(i * 20) / 13} width="30" height={20 / 13} fill="#b22234" />
          ))}
          <rect width="13" height={(20 * 7) / 13} fill="#3c3b6e" />
        </>
      )}
      {code === 'vi' && (
        <>
          <rect width="30" height="20" fill="#da251d" />
          <polygon points={star(15, 10.4, 6)} fill="#ffff00" />
        </>
      )}
      {code === 'ja' && (
        <>
          <rect width="30" height="20" fill="#fff" />
          <circle cx="15" cy="10" r="6" fill="#bc002d" />
        </>
      )}
      {code === 'zh' && (
        <>
          <rect width="30" height="20" fill="#ee1c25" />
          <polygon points={star(5, 5, 3)} fill="#ffde00" />
          {[
            [10, 2],
            [12, 4],
            [12, 7],
            [10, 9],
          ].map(([x, y]) => (
            <polygon key={`${x}-${y}`} points={star(x, y, 1)} fill="#ffde00" />
          ))}
        </>
      )}
    </svg>
  );
}
