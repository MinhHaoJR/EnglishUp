import { useCallback, useEffect, useRef, useState } from 'react';
import type { KeyboardEvent, PointerEvent } from 'react';

/** Size of the round chat head and the gap between it and the chat window, in pixels. */
export const HEAD = 60;
const GAP = 12;
/** A press that travels further than this is a drag, not a click. */
const DRAG_START = 6;
/** One arrow key press moves the head this far; with Shift, four times as far. */
export const STEP = 24;
const STORAGE_KEY = 'englishup.tutorPosition';

/**
 * Where the head sits, as a share of the free space: 0 is the left or top edge, 1 the right or bottom.
 * Shares rather than pixels keep it in the same corner or spot when the window is resized.
 */
export type Spot = { x: number; y: number };
export const CORNER: Spot = { x: 1, y: 1 };
type Box = { left: number; top: number };

const share = (n: number) => Math.min(1, Math.max(0, n));
/** Distance kept from the window's edges; matches the corner the head started in. */
export const edgeFor = (width: number) => (width <= 760 ? 16 : 20);

/** The head's pixel position for a spot in a window of this size. */
export function headBox(spot: Spot, width: number, height: number): Box {
  const edge = edgeFor(width);
  return {
    left: edge + spot.x * Math.max(0, width - HEAD - 2 * edge),
    top: edge + spot.y * Math.max(0, height - HEAD - 2 * edge),
  };
}

/** The spot for a pixel position, kept inside the window. */
export function spotFor(left: number, top: number, width: number, height: number): Spot {
  const edge = edgeFor(width);
  return {
    x: share((left - edge) / Math.max(1, width - HEAD - 2 * edge)),
    y: share((top - edge) / Math.max(1, height - HEAD - 2 * edge)),
  };
}

/**
 * The chat window beside the head: above it when there is more room above, otherwise below, and
 * lined up with the head's outer side, so it opens towards the middle of the screen. It shrinks to
 * fit the room it has and never leaves the window.
 */
export function panelBox(head: Box, width: number, height: number) {
  const edge = edgeFor(width);
  const panelWidth = Math.min(400, width - 32);
  const wanted = Math.min(680, height - 110);
  const above = head.top - GAP - edge;
  const below = height - (head.top + HEAD) - GAP - edge;
  const up = above >= below;
  const panelHeight = Math.max(Math.min(wanted, up ? above : below), Math.min(wanted, 320));
  const top = up ? head.top - GAP - panelHeight : head.top + HEAD + GAP;
  const onRight = head.left + HEAD / 2 > width / 2;
  const left = onRight ? head.left + HEAD - panelWidth : head.left;
  return {
    left: Math.min(Math.max(left, 16), width - panelWidth - 16),
    top: Math.min(Math.max(top, edge), height - panelHeight - edge),
    width: panelWidth,
    height: panelHeight,
  };
}

function readSpot(): Spot {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null') as Partial<Spot> | null;
    if (typeof saved?.x === 'number' && typeof saved.y === 'number')
      return { x: share(saved.x), y: share(saved.y) };
  } catch {
    // Storage can be blocked or hold something else; the corner is fine then.
  }
  return CORNER;
}
function saveSpot(spot: Spot) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(spot));
  } catch {
    // Not remembered in this browser; the head still moves for this visit.
  }
}

function useWindowSize() {
  const [size, setSize] = useState(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
  }));
  useEffect(() => {
    const resize = () => setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, []);
  return size;
}

/**
 * Lets the learner drag the chat head anywhere in the window (mouse, pen or touch) or move it with
 * the arrow keys; Home puts it back in the corner. The spot is remembered in this browser only, since
 * screens differ between devices. A press that does not travel stays a click.
 */
export function useChatHead() {
  const { width, height } = useWindowSize();
  const [spot, setSpot] = useState(readSpot);
  const [dragging, setDragging] = useState(false);
  const press = useRef<{ id: number; x: number; y: number; from: Box; moved: boolean } | null>(
    null,
  );
  const swallowClick = useRef(false);
  const head = headBox(spot, width, height);

  const moveTo = useCallback(
    (left: number, top: number, remember: boolean) => {
      const next = spotFor(left, top, width, height);
      setSpot(next);
      if (remember) saveSpot(next);
      return next;
    },
    [width, height],
  );

  const handlers = {
    onPointerDown(e: PointerEvent<HTMLButtonElement>) {
      if (e.button !== 0) return;
      swallowClick.current = false;
      press.current = { id: e.pointerId, x: e.clientX, y: e.clientY, from: head, moved: false };
      e.currentTarget.setPointerCapture?.(e.pointerId);
    },
    onPointerMove(e: PointerEvent<HTMLButtonElement>) {
      const p = press.current;
      if (!p || p.id !== e.pointerId) return;
      const dx = e.clientX - p.x;
      const dy = e.clientY - p.y;
      // Written so that a missing coordinate (NaN) never counts as a drag.
      if (!(Math.hypot(dx, dy) >= DRAG_START) && !p.moved) return;
      if (!Number.isFinite(dx) || !Number.isFinite(dy)) return;
      if (!p.moved) setDragging(true);
      p.moved = true;
      moveTo(p.from.left + dx, p.from.top + dy, false);
    },
    onPointerUp(e: PointerEvent<HTMLButtonElement>) {
      const p = press.current;
      if (!p || p.id !== e.pointerId) return;
      press.current = null;
      if (!p.moved) return;
      // The click that follows a drag must not open or close the chat.
      swallowClick.current = true;
      setDragging(false);
      moveTo(p.from.left + e.clientX - p.x, p.from.top + e.clientY - p.y, true);
    },
    onPointerCancel() {
      press.current = null;
      setDragging(false);
      saveSpot(spot);
    },
    onKeyDown(e: KeyboardEvent<HTMLButtonElement>) {
      const step = e.shiftKey ? STEP * 4 : STEP;
      const moves: Record<string, [number, number]> = {
        ArrowLeft: [-step, 0],
        ArrowRight: [step, 0],
        ArrowUp: [0, -step],
        ArrowDown: [0, step],
      };
      if (e.key === 'Home') {
        e.preventDefault();
        setSpot(CORNER);
        saveSpot(CORNER);
      } else if (moves[e.key]) {
        e.preventDefault();
        const [dx, dy] = moves[e.key];
        moveTo(head.left + dx, head.top + dy, true);
      }
    },
  };

  /** True once for the click that ends a drag; the caller skips that click. */
  const clickWasDrag = () => {
    const was = swallowClick.current;
    swallowClick.current = false;
    return was;
  };

  return { head, panel: panelBox(head, width, height), dragging, handlers, clickWasDrag };
}
