import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Vocabulary from '../features/vocabulary/Vocabulary';
import { vocabulary } from '../data/content';
import { useApp } from '../app/store';
import { defaults, db, resetData } from '../services/storage';
import { exportCSV, importCSV } from '../services/csv';

beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en' },
    level: 'all',
    topic: 'all',
    ready: true,
  });
});

test('specialist section opens Marketing cards in a fixed twenty-word study group', async () => {
  render(
    <MemoryRouter>
      <Vocabulary />
    </MemoryRouter>,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Specialist' }));
  expect(screen.getByRole('button', { name: /Marketing: Strategy 20 words/ })).toBeEnabled();
  expect(screen.queryByRole('button', { name: /People and family/ })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /Marketing: Strategy 20 words/ }));
  expect(screen.getByRole('heading', { name: 'Marketing: Strategy' })).toBeInTheDocument();
  const group = screen.getByRole('radiogroup', { name: 'Word group' });
  await waitFor(() => expect(within(group).getAllByRole('radio')[0]).toBeEnabled());
  expect(within(group).getAllByRole('radio')).toHaveLength(1);
  const start = screen.getByRole('button', { name: /Start practice/ });
  fireEvent.click(start);
  await screen.findByRole('heading', { name: 'positioning' });
  fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  await screen.findByRole('heading', { name: 'buyer persona' });
  expect(await db.attempts.count()).toBe(0);
});

test('C2 exam topics remain browsable and their cards export with exact level and topic', async () => {
  render(
    <MemoryRouter>
      <Vocabulary />
    </MemoryRouter>,
  );
  fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'C2' } });
  fireEvent.click(screen.getByRole('button', { name: 'Advanced exam' }));
  const academic = screen.getByRole('button', { name: /Exam: Academic argument 10 words/ });
  fireEvent.click(academic);
  expect(screen.getByRole('heading', { name: 'Exam: Academic argument' })).toBeInTheDocument();
  const selected = vocabulary.filter(
    (word) => word.level === 'C2' && word.topic === 'Exam: Academic argument',
  );
  expect(selected).toHaveLength(10);
  const rows = importCSV(exportCSV(selected));
  expect(rows.map((word) => word.word)).toEqual(selected.map((word) => word.word));
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  fireEvent.change(screen.getByRole('searchbox', { name: 'Search words' }), {
    target: { value: 'epistemic limit' },
  });
  expect(screen.getByRole('heading', { name: /epistemic limit/ })).toBeInTheDocument();
});

test('IT topics expose new cards in twenty-word groups without recording a skipped answer', async () => {
  render(
    <MemoryRouter>
      <Vocabulary />
    </MemoryRouter>,
  );
  fireEvent.click(screen.getByRole('button', { name: 'Specialist' }));
  fireEvent.click(screen.getByRole('button', { name: /IT: Programming 30 words/ }));
  const group = screen.getByRole('radiogroup', { name: 'Word group' });
  await waitFor(() => expect(within(group).getAllByRole('radio')[1]).toBeEnabled());
  const stations = within(group).getAllByRole('radio');
  expect(stations).toHaveLength(2);
  fireEvent.click(stations[1]);
  await waitFor(() => expect(stations[1]).toHaveAttribute('aria-checked', 'true'));
  fireEvent.click(screen.getByRole('button', { name: /Start practice/ }));
  await screen.findByRole('heading', { name: 'class definition' });
  fireEvent.click(screen.getByRole('button', { name: 'Skip word →' }));
  await screen.findByRole('heading', { name: 'object instance' });
  expect(await db.attempts.count()).toBe(0);
});
