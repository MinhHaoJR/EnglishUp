/** Advance within the current filtered list; the final lesson returns to the list. */
export function nextLesson<T extends { id: string }>(
  items: readonly T[],
  current: T,
): T | undefined {
  const index = items.findIndex((item) => item.id === current.id);
  return index < 0 ? undefined : items[index + 1];
}
