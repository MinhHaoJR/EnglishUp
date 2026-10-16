import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Vocabulary from '../features/vocabulary/Vocabulary';
import { db, defaults, resetData, exportData, importData } from '../services/storage';
import { useApp } from '../app/store';
import { vocabulary } from '../data/content';
import { studyScope } from '../services/vocabularyStudy';

const words = vocabulary.filter(
  (word) => word.topic === 'People and family' && word.level === 'A1',
);
beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en', newCards: 0 },
    level: 'A1',
    topic: 'People and family',
    ready: true,
  });
});
function show() {
  return render(
    <MemoryRouter>
      <Vocabulary />
    </MemoryRouter>,
  );
}
async function start() {
  const button = screen.getByRole('button', { name: /Start practice/ });
  await waitFor(() => expect(button).toBeEnabled(), { timeout: 4000 });
  fireEvent.click(button);
  await screen.findByRole('button', { name: 'Reveal answer' }, { timeout: 4000 });
}

test('twenty-word groups can be selected with a zero legacy daily limit and resume after skip, early exit and backup', async () => {
  let view = show();
  const select = screen.getByRole('combobox', { name: 'Word group' });
  await waitFor(() => expect(select).toBeEnabled());
  expect(select.querySelectorAll('option')).toHaveLength(2);
  fireEvent.change(select, { target: { value: words[20].id } });
  await waitFor(() => expect(select).toHaveValue(words[20].id));
  await start();
  expect(screen.getByRole('heading', { name: words[20].word })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  await screen.findByRole('heading', { name: words[21].word });
  expect(await db.attempts.count()).toBe(0);
  expect(await db.reviews.count()).toBe(0);
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await screen.findByRole('heading', { name: words[22].word });
  fireEvent.click(screen.getByRole('button', { name: 'End early (keep progress)' }));
  await start();
  expect(screen.getByRole('heading', { name: words[22].word })).toBeInTheDocument();
  view.unmount();
  const snapshot = await exportData();
  await resetData();
  await importData(snapshot);
  view = show();
  await start();
  expect(screen.getByRole('heading', { name: words[22].word })).toBeInTheDocument();
  expect(await db.attempts.count()).toBe(1);
  view.unmount();
}, 15000);

test('skip is guarded against double clicks and a failed save keeps the current word', async () => {
  show();
  await start();
  vi.spyOn(db.vocabularyStudy, 'put').mockRejectedValueOnce(new Error('storage full'));
  fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Could not save progress');
  expect(screen.getByRole('heading', { name: words[0].word })).toBeInTheDocument();
  const skip = screen.getByRole('button', { name: 'Skip word →' });
  fireEvent.click(skip);
  fireEvent.click(skip);
  await screen.findByRole('heading', { name: words[1].word });
  expect((await db.vocabularyStudy.get(studyScope('A1', 'People and family')))?.visitedIds).toEqual(
    [words[0].id],
  );
});

test('finishing twenty skipped cards opens another group immediately without scoring or revealing them', async () => {
  show();
  await start();
  for (let index = 0; index < 20; index++) {
    await screen.findByRole('heading', { name: words[index].word });
    fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  }
  await screen.findByRole('heading', { name: 'Session complete' });
  expect(await db.attempts.count()).toBe(0);
  expect(screen.getByRole('button', { name: 'Review this group →' })).toBeEnabled();
  fireEvent.click(screen.getByRole('button', { name: 'Study next group →' }));
  await screen.findByRole('heading', { name: words[20].word });
});

test('changing practice mode preserves the next word and typing starts with a fresh answer', async () => {
  show();
  await start();
  fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  await screen.findByRole('heading', { name: words[1].word });
  fireEvent.click(screen.getByRole('button', { name: 'End early (keep progress)' }));
  fireEvent.change(screen.getByRole('combobox', { name: 'Practice mode' }), {
    target: { value: 'type' },
  });
  const button = screen.getByRole('button', { name: /Start practice/ });
  await waitFor(() => expect(button).toBeEnabled());
  fireEvent.click(button);
  await screen.findByRole('heading', { name: words[1].meaning });
  expect(screen.getByRole('textbox', { name: 'Your answer' })).toHaveValue('');
  fireEvent.change(screen.getByRole('textbox', { name: 'Your answer' }), {
    target: { value: words[1].word },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await screen.findByRole('heading', { name: words[2].meaning });
  expect(screen.getByRole('textbox', { name: 'Your answer' })).toHaveValue('');
});
