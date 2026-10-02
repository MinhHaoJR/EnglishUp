import { render, screen, waitFor, fireEvent, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import Vocabulary from '../features/vocabulary/Vocabulary';
import Reading from '../features/reading/Reading';
import Listening from '../features/listening/Listening';
import Speaking from '../features/speaking/Speaking';
import Writing from '../features/writing/Writing';
import Dashboard from '../features/dashboard/Dashboard';
import { readings, listenings } from '../data/content';
beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en', newCards: 1 },
    level: 'all',
    topic: 'all',
    ready: true,
  });
});
function show(element: React.ReactNode) {
  return render(<MemoryRouter>{element}</MemoryRouter>);
}
async function verifyAttempt(skill: string) {
  await waitFor(async () => expect(await db.attempts.where('skill').equals(skill).count()).toBe(1));
}
test('vocabulary completes a card, schedules it and persists the attempt', async () => {
  show(<Vocabulary />);
  fireEvent.click(screen.getByRole('button', { name: /Start practice/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await screen.findByRole('heading', { name: 'Session complete' });
  await verifyAttempt('vocabulary');
  expect(await db.reviews.count()).toBe(1);
});
test('reading completes all question types, shows evidence and logs score', async () => {
  show(<Reading />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  for (const q of readings[0].questions) {
    if (q.type === 'short')
      fireEvent.change(screen.getByRole('textbox'), { target: { value: q.answers[0] } });
    else
      fireEvent.click(
        within(
          screen.getByRole('group', {
            name: `${readings[0].questions.indexOf(q) + 1}. ${q.prompt}`,
          }),
        ).getByRole('radio', { name: q.answers[0] }),
      );
  }
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  await verifyAttempt('reading');
  expect((await db.attempts.toArray())[0].score).toBe(100);
  expect(await screen.findByText(/Session complete · 100/)).toBeInTheDocument();
});
test('listening gates transcript until answers are submitted', async () => {
  show(<Listening />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  expect(screen.getByText('The transcript unlocks after you answer.')).toBeInTheDocument();
  const boxes = screen.getAllByRole('textbox');
  let i = 0;
  for (const q of listenings[0].questions) {
    if (q.type === 'blank') fireEvent.change(boxes[i++], { target: { value: q.answers[0] } });
    else fireEvent.click(screen.getByRole('radio', { name: q.answers[0] }));
  }
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  await verifyAttempt('listening');
  expect(await screen.findByRole('heading', { name: 'Transcript' })).toBeInTheDocument();
});
test('speaking unsupported-API flow completes with explicit self-assessment', async () => {
  show(<Speaking />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  expect(screen.getByText(/Recognition is unsupported/)).toBeInTheDocument();
  fireEvent.click(screen.getByLabelText('I said all the words.'));
  fireEvent.click(screen.getByLabelText('I practiced aloud and completed my self-assessment.'));
  fireEvent.click(screen.getByRole('button', { name: 'Finish session' }));
  await verifyAttempt('speaking');
  expect((await db.attempts.toArray())[0].label).toContain('self-assessed');
});
test('writing autosaves, submits feedback, and restores a draft after remount', async () => {
  const view = show(<Writing />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  const editor = screen.getByRole('textbox', { name: 'Draft' });
  await waitFor(() => expect(editor).toBeEnabled());
  const text =
    'Dear Mai, I am agree with your plan. We can visit the park because the weather is nice. Shall we meet at three?';
  fireEvent.change(editor, { target: { value: text } });
  await waitFor(async () => expect((await db.drafts.get('w1'))?.text).toBe(text));
  fireEvent.click(screen.getByRole('button', { name: 'Get feedback & save' }));
  await verifyAttempt('writing');
  expect(await db.submissions.count()).toBe(1);
  expect(screen.getByRole('region', { name: 'Feedback' })).toHaveTextContent('Agree is a verb');
  view.unmount();
  show(<Writing />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  await waitFor(() => expect(screen.getByRole('textbox', { name: 'Draft' })).toHaveValue(text));
});
test('dashboard reconstructs progress from persisted attempts after remount', async () => {
  await db.attempts.add({
    id: 'saved',
    skill: 'reading',
    score: 80,
    duration: 120,
    timestamp: Date.now(),
    label: 'Persisted reading',
  });
  let view = show(<Dashboard />);
  expect(await screen.findByText('Persisted reading')).toBeInTheDocument();
  view.unmount();
  view = show(<Dashboard />);
  expect(await screen.findByText('Persisted reading')).toBeInTheDocument();
  expect(screen.getByRole('progressbar', { name: 'Daily goal' })).toHaveAttribute('value', '20');
  view.unmount();
});
