import { render, screen, waitFor, fireEvent, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData, exportData, importData } from '../services/storage';
import Vocabulary from '../features/vocabulary/Vocabulary';
import Reading from '../features/reading/Reading';
import Listening from '../features/listening/Listening';
import Speaking from '../features/speaking/Speaking';
import Writing from '../features/writing/Writing';
import Dashboard from '../features/dashboard/Dashboard';
import { readings, listenings, vocabulary } from '../data/content';
import { exportCSV, importCSV } from '../services/csv';
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

test('large library pages are bounded and search and topic changes return to page one', () => {
  show(<Vocabulary />);
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  expect(screen.getAllByRole('article')).toHaveLength(30);
  fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
  expect(screen.getByText('Page 2/52 · 1560 matching words')).toBeInTheDocument();
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'pineapple' } });
  expect(screen.getAllByRole('article')).toHaveLength(1);
  expect(screen.getByRole('heading', { name: /pineapple/ })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Previous page' })).toBeDisabled();
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: '' } });
  expect(screen.getByText('Page 1/52 · 1560 matching words')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'People and family · 50' }));
  expect(screen.getByText('Page 1/2 · 50 matching words')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
  expect(screen.getAllByRole('article')).toHaveLength(20);
  expect(screen.getByRole('button', { name: 'Next page' })).toBeDisabled();
  fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'A2' } });
  expect(screen.getAllByRole('article')).toHaveLength(10);
  expect(screen.getByRole('button', { name: 'Previous page' })).toBeDisabled();
});

test('a new A1 card persists through backup, reset and restore; CSV includes a whole topic', async () => {
  useApp.setState({ level: 'A1', topic: 'People and family' });
  const view = show(<Vocabulary />);
  fireEvent.click(screen.getByRole('button', { name: /Start practice/ }));
  expect(screen.getByRole('heading', { name: 'person' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await verifyAttempt('vocabulary');
  view.unmount();
  const snapshot = await exportData();
  await resetData();
  await importData(snapshot);
  expect(await db.reviews.get('v-common-person')).toMatchObject({ total: 1, correct: 1 });
  expect((await db.attempts.toArray())[0].label).toBe('person');
  const topic = vocabulary.filter((word) => word.topic === 'People and family');
  const imported = importCSV(exportCSV(topic));
  expect(imported).toHaveLength(50);
  expect(imported.map((word) => word.word)).toEqual(topic.map((word) => word.word));
});

test('IT topics filter the library and practice, and persist a review across remount', async () => {
  let view = show(<Vocabulary />);
  fireEvent.click(screen.getByRole('button', { name: 'IT: Programming · 10' }));
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  const group = screen.getByRole('region', { name: 'IT: Programming' });
  expect(within(group).getAllByRole('article')).toHaveLength(10);
  expect(screen.queryByRole('region', { name: 'Daily life' })).not.toBeInTheDocument();
  fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'B1' } });
  expect(within(group).getAllByRole('article')).toHaveLength(5);
  fireEvent.click(screen.getByRole('button', { name: 'Practice' }));
  fireEvent.click(screen.getByRole('button', { name: /Start practice/ }));
  expect(screen.getByRole('heading', { name: 'variable' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await verifyAttempt('vocabulary');
  expect(await db.reviews.get('v-extra-variable')).toMatchObject({ total: 1 });
  view.unmount();
  view = show(<Vocabulary />);
  await waitFor(() =>
    expect(screen.getByRole('button', { name: /Start practice/ })).toBeDisabled(),
  );
  expect((await db.attempts.toArray())[0].label).toBe('variable');
  view.unmount();
});

test('Vietnamese topics and accent-free search include custom imported topics', async () => {
  useApp.setState({ settings: { ...defaults, language: 'vi' } });
  await db.words.add({
    id: 'custom-topic',
    word: 'widget',
    ipa: '',
    pos: 'noun',
    meaning: 'tiện ích',
    definition: 'a small interface element',
    examples: ['Add a widget to the page.'],
    level: 'B1',
    topic: 'My project',
    custom: true,
  });
  show(<Vocabulary />);
  expect(await screen.findByRole('button', { name: 'My project · 1' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'IT: Cơ sở dữ liệu · 10' }));
  fireEvent.click(screen.getByRole('button', { name: /Sổ từ vựng/ }));
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'co so du lieu' } });
  expect(screen.getByRole('heading', { name: /database/ })).toBeInTheDocument();
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'not-a-word' } });
  expect(screen.queryAllByRole('article')).toHaveLength(0);
  fireEvent.click(screen.getByRole('button', { name: 'Xóa tìm kiếm' }));
  expect(screen.getAllByRole('article')).toHaveLength(10);
  fireEvent.change(screen.getByRole('combobox', { name: 'Chủ đề' }), {
    target: { value: 'My project' },
  });
  expect(screen.getAllByRole('article')).toHaveLength(1);
  expect(screen.getByRole('heading', { name: /widget/ })).toBeInTheDocument();
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
