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
import {
  readings,
  listenings,
  vocabulary,
  speakingPrompts,
  writingPrompts,
  dictations,
} from '../data/content';
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
async function startVocabulary() {
  const button = screen.getByRole('button', { name: /Start practice/ });
  await waitFor(() => expect(button).toBeEnabled(), { timeout: 4000 });
  fireEvent.click(button);
  await screen.findByRole('button', { name: 'Reveal answer' }, { timeout: 4000 });
}
async function verifyAttempt(skill: string) {
  await waitFor(async () => expect(await db.attempts.where('skill').equals(skill).count()).toBe(1));
}
test('vocabulary advances a card, schedules it and persists the attempt', async () => {
  show(<Vocabulary />);
  await startVocabulary();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await screen.findByRole('heading', { name: vocabulary[1].word });
  await verifyAttempt('vocabulary');
  expect(await db.reviews.count()).toBe(1);
}, 12000);

test('large library pages are bounded and search and topic changes return to page one', () => {
  show(<Vocabulary />);
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  expect(screen.getAllByRole('article')).toHaveLength(30);
  fireEvent.click(screen.getByRole('button', { name: 'Next page' }));
  expect(screen.getByText('Page 2/70 · 2080 matching words')).toBeInTheDocument();
  fireEvent.change(screen.getByRole('searchbox', { name: 'Search words' }), {
    target: { value: 'pineapple' },
  });
  expect(screen.getAllByRole('article')).toHaveLength(1);
  expect(screen.getByRole('heading', { name: /pineapple/ })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Previous page' })).toBeDisabled();
  fireEvent.change(screen.getByRole('searchbox', { name: 'Search words' }), {
    target: { value: '' },
  });
  expect(screen.getByText('Page 1/70 · 2080 matching words')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'People and family 50 words' }));
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
  await startVocabulary();
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
  fireEvent.click(screen.getByRole('button', { name: 'Specialist' }));
  fireEvent.click(screen.getByRole('button', { name: 'IT: Programming 30 words' }));
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  const group = screen.getByRole('region', { name: 'IT: Programming' });
  expect(within(group).getAllByRole('article')).toHaveLength(30);
  expect(screen.queryByRole('region', { name: 'Daily life' })).not.toBeInTheDocument();
  fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'B1' } });
  expect(within(group).getAllByRole('article')).toHaveLength(15);
  fireEvent.click(screen.getByRole('button', { name: 'Practice' }));
  await startVocabulary();
  expect(screen.getByRole('heading', { name: 'variable' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await verifyAttempt('vocabulary');
  expect(await db.reviews.get('v-extra-variable')).toMatchObject({ total: 1 });
  view.unmount();
  view = show(<Vocabulary />);
  await startVocabulary();
  const nextWord = vocabulary.filter(
    (word) => word.topic === 'IT: Programming' && word.level === 'B1',
  )[1];
  expect(screen.getByRole('heading', { name: nextWord.word })).toBeInTheDocument();
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
  fireEvent.click(await screen.findByRole('button', { name: 'Tự thêm' }));
  expect(screen.getByRole('button', { name: 'My project 1 từ' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Chuyên ngành' }));
  fireEvent.click(screen.getByRole('button', { name: 'IT: Cơ sở dữ liệu 30 từ' }));
  fireEvent.click(screen.getByRole('button', { name: /Sổ từ vựng/ }));
  fireEvent.change(screen.getByRole('searchbox', { name: 'Tìm từ vựng' }), {
    target: { value: 'co so du lieu' },
  });
  expect(screen.getAllByRole('heading', { name: /database/ }).length).toBeGreaterThan(0);
  fireEvent.change(screen.getByRole('searchbox', { name: 'Tìm từ vựng' }), {
    target: { value: 'not-a-word' },
  });
  expect(screen.queryAllByRole('article')).toHaveLength(0);
  fireEvent.click(screen.getByRole('button', { name: 'Xóa tìm kiếm' }));
  expect(screen.getAllByRole('article')).toHaveLength(30);
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
  fireEvent.click(screen.getByRole('button', { name: 'Continue →' }));
  expect(screen.getByRole('heading', { name: readings[1].title })).toBeInTheDocument();
  expect(screen.queryByText(/Session complete/)).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: 'Check answer' })).toBeDisabled();
  expect(await db.attempts.count()).toBe(1);
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
  fireEvent.click(screen.getByRole('button', { name: 'Continue →' }));
  expect(screen.getByRole('heading', { name: listenings[1].title })).toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: 'Transcript' })).not.toBeInTheDocument();
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
  fireEvent.click(await screen.findByRole('button', { name: 'Continue →' }));
  expect(
    screen.getByRole('heading', {
      name: speakingPrompts.filter((p) => p.mode === 'read')[1].title,
    }),
  ).toBeInTheDocument();
  expect(
    screen.getByLabelText('I practiced aloud and completed my self-assessment.'),
  ).not.toBeChecked();
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

test('dashboard plan puts due cards first and then the weakest skill', async () => {
  const yesterday = Date.now() - 86_400_000;
  await db.attempts.bulkAdd(
    (['vocabulary', 'listening', 'speaking', 'reading', 'writing', 'grammar'] as const).map(
      (skill) => ({
        id: skill,
        skill,
        score: skill === 'listening' ? 40 : 95,
        duration: 60,
        timestamp: yesterday,
        label: skill,
      }),
    ),
  );
  await db.reviews.add({
    id: vocabulary[0].id,
    ease: 2.5,
    interval: 1,
    repetitions: 1,
    due: yesterday,
    introduced: yesterday,
    lastReviewed: yesterday,
    correct: 1,
    total: 1,
  });
  show(<Dashboard />);
  const plan = within(
    (await screen.findByRole('heading', { name: 'Your plan for today' })).closest('section')!,
  );
  await waitFor(() => expect(plan.getAllByRole('link')[1]).toHaveTextContent('Recent score 40%'));
  expect(plan.getAllByRole('link')[0]).toHaveTextContent('1 card due for review');
  expect(plan.getAllByRole('link')[1]).toHaveAttribute('href', '/listening');
});

test('continue writing opens the next prompt and keeps the saved draft and attempt', async () => {
  show(<Writing />);
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  const editor = screen.getByRole('textbox', { name: 'Draft' });
  await waitFor(() => expect(editor).toBeEnabled());
  fireEvent.change(editor, { target: { value: 'Dear Mai, let us meet in the park tomorrow.' } });
  expect(screen.queryByRole('button', { name: 'Continue →' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Get feedback & save' }));
  fireEvent.click(await screen.findByRole('button', { name: 'Continue →' }));
  expect(screen.getByRole('heading', { name: writingPrompts[1].title })).toBeInTheDocument();
  await waitFor(() => expect(screen.getByRole('textbox', { name: 'Draft' })).toBeEnabled());
  expect(screen.getByRole('textbox', { name: 'Draft' })).toHaveValue('');
  expect(await db.attempts.count()).toBe(1);
  expect((await db.drafts.get(writingPrompts[0].id))?.text).toContain('Dear Mai');
});

test('dictation continues with an empty answer and the previous attempt saved', async () => {
  show(<Listening />);
  fireEvent.click(screen.getByRole('button', { name: 'Dictation' }));
  fireEvent.click(screen.getAllByRole('button', { name: /Start practice/ })[0]);
  fireEvent.change(screen.getByRole('textbox'), { target: { value: dictations[0].text } });
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  fireEvent.click(await screen.findByRole('button', { name: 'Continue →' }));
  expect(screen.getByRole('textbox')).toHaveValue('');
  fireEvent.change(screen.getByRole('textbox'), { target: { value: dictations[1].text } });
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  await waitFor(async () => expect(await db.attempts.count()).toBe(2));
  expect((await db.attempts.toArray()).map((a) => a.label)).toEqual(
    expect.arrayContaining([`Dictation ${dictations[0].id}`, `Dictation ${dictations[1].id}`]),
  );
});

test('the last filtered reading returns to lessons without starting an unrelated lesson', async () => {
  useApp.setState({
    level: readings[0].level,
    topic: readings[0].topic,
    settings: { ...defaults, language: 'vi' },
  });
  const filtered = readings.filter(
    (r) => r.level === readings[0].level && r.topic === readings[0].topic,
  );
  const last = filtered[filtered.length - 1];
  show(<Reading />);
  fireEvent.click(screen.getAllByRole('button', { name: /Bắt đầu luyện tập/ }).at(-1)!);
  expect(screen.queryByRole('button', { name: 'Tiếp tục →' })).not.toBeInTheDocument();
  for (const q of last.questions) {
    const group = screen.getByRole('group', {
      name: `${last.questions.indexOf(q) + 1}. ${q.prompt}`,
    });
    if (q.type === 'short' || q.type === 'blank')
      fireEvent.change(within(group).getByRole('textbox'), { target: { value: q.answers[0] } });
    else fireEvent.click(within(group).getByRole('radio', { name: q.answers[0] }));
  }
  fireEvent.click(screen.getByRole('button', { name: 'Kiểm tra' }));
  fireEvent.click(await screen.findByRole('button', { name: 'Về danh sách bài học →' }));
  expect(screen.getAllByRole('button', { name: /Bắt đầu luyện tập/ })).toHaveLength(
    filtered.length,
  );
  expect(await db.attempts.count()).toBe(1);
});

test('C1 vocabulary filters, exports and persists a review through backup and restore', async () => {
  const view = show(<Vocabulary />);
  fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'C1' } });
  fireEvent.change(screen.getByRole('combobox', { name: 'Topic' }), { target: { value: 'Work' } });
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  expect(screen.getAllByRole('article')).toHaveLength(10);
  expect(screen.getByRole('heading', { name: /accountability/ })).toBeInTheDocument();
  expect(screen.queryByRole('heading', { name: /workload/ })).not.toBeInTheDocument();
  const exported = importCSV(
    exportCSV(vocabulary.filter((w) => w.level === 'C1' && w.topic === 'Work')),
  );
  expect(exported).toHaveLength(10);
  expect(exported.every((word) => word.level === 'C1')).toBe(true);
  fireEvent.click(screen.getByRole('button', { name: 'Practice' }));
  await startVocabulary();
  expect(screen.getByRole('heading', { name: 'accountability' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Reveal answer' }));
  fireEvent.click(screen.getByRole('button', { name: 'Good' }));
  await verifyAttempt('vocabulary');
  view.unmount();
  const backup = await exportData();
  await resetData();
  await importData(backup);
  expect(await db.reviews.get('v-common-accountability')).toMatchObject({ total: 1, correct: 1 });
  expect((await db.attempts.toArray())[0].label).toBe('accountability');
});
