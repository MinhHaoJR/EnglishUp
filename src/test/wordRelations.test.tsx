import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import { wordRelations } from '../data/wordRelations';
import Vocabulary from '../features/vocabulary/Vocabulary';
import WordRelations from '../features/vocabulary/WordRelations';

beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en' },
    level: 'all',
    topic: 'all',
    ready: true,
  });
});

function currentAnswer(correct = true) {
  const word = document.querySelector('.relations-target')!.textContent;
  const entry = wordRelations.find((item) => item.word === word)!;
  const synonym = !!screen.queryByRole('heading', { name: 'Which word is closest in meaning?' });
  return (synonym === correct ? entry.synonyms : entry.antonyms)[0].word;
}

test('direct link opens the relation tab, with independent levels and bounded searchable pages', () => {
  useApp.setState({ level: 'A2', topic: 'Health' });
  render(
    <MemoryRouter initialEntries={['/vocabulary?tab=relations']}>
      <Vocabulary />
    </MemoryRouter>,
  );
  expect(screen.getByRole('button', { name: 'Synonyms & antonyms' })).toHaveAttribute(
    'aria-pressed',
    'true',
  );
  expect(screen.queryByRole('combobox', { name: 'Level' })).not.toBeInTheDocument();
  expect(screen.getAllByRole('article')).toHaveLength(12);
  expect(screen.getByText('Page 1 / 6')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Next →' }));
  expect(screen.getByText('Page 2 / 6')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /C2 Proficient 12 entries/ }));
  expect(screen.getAllByRole('article')).toHaveLength(12);
  const c2 = wordRelations.find((item) => item.level === 'C2')!;
  expect(screen.getByRole('heading', { name: c2.word })).toBeInTheDocument();
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'no-such-word-xyz' } });
  expect(screen.queryAllByRole('article')).toHaveLength(0);
  expect(screen.getByRole('button', { name: 'Practice 0 questions →' })).toBeDisabled();
  fireEvent.click(screen.getByRole('button', { name: 'Clear filters' }));
  expect(screen.getByText('Page 1 / 6')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /Word library/ }));
  expect(screen.getByRole('combobox', { name: 'Level' })).toHaveValue('A2');
});

test.each(['synonym', 'antonym'] as const)(
  '%s practice saves once, then continues with a fresh answer',
  async (mode) => {
    render(<WordRelations />);
    fireEvent.change(screen.getByRole('combobox', { name: 'Word relationship' }), {
      target: { value: mode },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Practice 10 questions →' }));
    expect(screen.queryByRole('searchbox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Check & save' })).toBeDisabled();
    const answer = currentAnswer();
    fireEvent.click(screen.getByRole('radio', { name: answer }));
    const submit = screen.getByRole('button', { name: 'Check & save' });
    fireEvent.click(submit);
    fireEvent.click(submit);
    await screen.findByText('Correct! Result saved.');
    expect(await db.attempts.count()).toBe(1);
    expect((await db.attempts.toArray())[0]).toMatchObject({
      score: 100,
      skill: 'vocabulary',
      learningLanguage: 'en',
    });
    expect(screen.getByRole('radio', { name: answer })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Continue →' }));
    expect(screen.getByRole('button', { name: 'Check & save' })).toBeDisabled();
    expect(screen.queryByText('Correct! Result saved.')).not.toBeInTheDocument();
    expect(
      screen.getByRole('heading', {
        name:
          mode === 'synonym'
            ? 'Which word is closest in meaning?'
            : 'Which word has the opposite meaning?',
      }),
    ).toHaveFocus();
    fireEvent.click(screen.getByRole('button', { name: '← Back to word library' }));
    expect(await db.attempts.count()).toBe(1);
    expect(await db.reviews.count()).toBe(0);
  },
);

test('failed save preserves the selected answer and only a successful retry enables continuation', async () => {
  render(<WordRelations />);
  fireEvent.click(screen.getByRole('button', { name: 'Practice 10 questions →' }));
  const wrong = currentAnswer(false);
  fireEvent.click(screen.getByRole('radio', { name: wrong }));
  vi.spyOn(db.attempts, 'add').mockRejectedValueOnce(new Error('storage unavailable'));
  fireEvent.click(screen.getByRole('button', { name: 'Check & save' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('could not be saved');
  expect(screen.queryByRole('button', { name: 'Continue →' })).not.toBeInTheDocument();
  expect(screen.getByRole('radio', { name: wrong })).toBeChecked();
  expect(await db.attempts.count()).toBe(0);
  fireEvent.click(screen.getByRole('button', { name: 'Retry saving' }));
  await screen.findByText('Result saved. Let’s review it.');
  expect((await db.attempts.toArray())[0].score).toBe(0);
  fireEvent.click(screen.getByRole('button', { name: 'Continue →' }));
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});

test('a mixed session completes all ten answers and persists them across remount', async () => {
  const view = render(<WordRelations />);
  fireEvent.click(screen.getByRole('button', { name: /B2 Upper intermediate 12 entries/ }));
  fireEvent.click(screen.getByRole('button', { name: 'Practice 10 questions →' }));
  for (let index = 0; index < 10; index++) {
    fireEvent.click(screen.getByRole('radio', { name: currentAnswer() }));
    fireEvent.click(screen.getByRole('button', { name: 'Check & save' }));
    await screen.findByText('Correct! Result saved.');
    fireEvent.click(
      screen.getByRole('button', { name: index === 9 ? 'See results →' : 'Continue →' }),
    );
  }
  expect(screen.getByRole('heading', { name: 'Practice complete!' })).toHaveFocus();
  const attempts = await db.attempts.toArray();
  expect(attempts).toHaveLength(10);
  expect(attempts.every((attempt) => attempt.score === 100 && attempt.label.includes('B2:'))).toBe(
    true,
  );
  expect(attempts.filter((attempt) => attempt.label.startsWith('Synonym'))).toHaveLength(5);
  expect(attempts.filter((attempt) => attempt.label.startsWith('Antonym'))).toHaveLength(5);
  view.unmount();
  render(<WordRelations />);
  await waitFor(async () => expect(await db.attempts.count()).toBe(10));
});
