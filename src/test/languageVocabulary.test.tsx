import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi } from 'vitest';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';
import { languageVocabulary } from '../data/languageVocabulary';
import LanguageVocabulary from '../features/languages/LanguageVocabulary';
import LanguageWorkspace from '../features/languages/LanguageWorkspace';

beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en', learningLanguage: 'ja' },
    ready: true,
  });
});

test.each(['ja', 'zh'] as const)('%s library pages and searches its own catalog', (language) => {
  useApp.setState({ settings: { ...defaults, language: 'en', learningLanguage: language } });
  render(
    <MemoryRouter>
      <LanguageWorkspace skill="vocabulary" />
    </MemoryRouter>,
  );
  expect(screen.getAllByRole('article')).toHaveLength(24);
  fireEvent.click(screen.getByRole('button', { name: 'Next page →' }));
  expect(screen.getByRole('combobox', { name: 'Choose page' })).toHaveValue('2');
  const word = languageVocabulary.find((word) => word.language === language)!;
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: word.text } });
  expect(screen.getByRole('heading', { name: word.text })).toBeInTheDocument();
  const page = screen.queryByRole('combobox', { name: 'Choose page' });
  if (page) expect(page).toHaveValue('1');
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'zzzz-no-such-word' } });
  expect(screen.queryAllByRole('article')).toHaveLength(0);
  expect(screen.getByRole('button', { name: /Practice 10 words/ })).toBeDisabled();
  fireEvent.click(screen.getByRole('button', { name: 'Clear search and filters' }));
  expect(screen.getAllByRole('article')).toHaveLength(24);
});

test('topic deep links open the requested collection and topic changes reset pagination', () => {
  render(
    <MemoryRouter initialEntries={['/vocabulary?topic=food']}>
      <LanguageVocabulary language="ja" />
    </MemoryRouter>,
  );
  const expected = languageVocabulary.filter(
    (word) => word.language === 'ja' && word.topic === 'food',
  );
  expect(screen.getByRole('heading', { name: expected[0].text })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Next page →' }));
  fireEvent.click(screen.getByRole('button', { name: /People & family/ }));
  expect(screen.getByRole('combobox', { name: 'Choose page' })).toHaveValue('1');
});

test.each(['ja', 'zh'] as const)(
  '%s saves a word once and continues with a fresh question',
  async (language) => {
    useApp.setState({ settings: { ...defaults, language: 'en', learningLanguage: language } });
    render(
      <MemoryRouter>
        <LanguageVocabulary language={language} />
      </MemoryRouter>,
    );
    const word = languageVocabulary.find((word) => word.language === language)!;
    fireEvent.click(screen.getByRole('button', { name: `Learn word: ${word.text}` }));
    const submit = screen.getByRole('button', { name: 'Check & save' });
    expect(submit).toBeDisabled();
    fireEvent.click(screen.getByRole('radio', { name: word.meaning.en }));
    fireEvent.click(submit);
    fireEvent.click(submit);
    await screen.findByText(/Result saved/);
    expect(await db.attempts.count()).toBe(1);
    expect((await db.attempts.toArray())[0]).toMatchObject({
      learningLanguage: language,
      score: 100,
      label: word.text,
    });
    fireEvent.click(screen.getByRole('button', { name: 'Continue →' }));
    expect(screen.getByRole('button', { name: 'Check & save' })).toBeDisabled();
    expect(screen.queryByText(/Result saved/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: '← Back to library' }));
    expect(await screen.findByText('Practiced')).toBeInTheDocument();
  },
);

test('a failed save retains the answer and retry completes without losing progress', async () => {
  const word = languageVocabulary.find((word) => word.language === 'ja')!;
  render(
    <MemoryRouter>
      <LanguageVocabulary language="ja" />
    </MemoryRouter>,
  );
  fireEvent.click(screen.getByRole('button', { name: `Learn word: ${word.text}` }));
  fireEvent.click(screen.getByRole('radio', { name: word.meaning.en }));
  const add = vi.spyOn(db.attempts, 'add').mockRejectedValueOnce(new Error('storage unavailable'));
  fireEvent.click(screen.getByRole('button', { name: 'Check & save' }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Could not save');
  expect(screen.queryByRole('button', { name: 'Continue →' })).not.toBeInTheDocument();
  expect(screen.getByRole('radio', { name: word.meaning.en })).toBeChecked();
  fireEvent.click(screen.getByRole('button', { name: 'Check & save' }));
  await waitFor(async () => expect(await db.attempts.count()).toBe(1));
  expect(await screen.findByText(/Result saved/)).toBeInTheDocument();
  add.mockRestore();
});

test('a filtered one-word session reaches results and retains progress after remount', async () => {
  const word = languageVocabulary.find((word) => word.language === 'ja')!;
  const view = render(
    <MemoryRouter>
      <LanguageVocabulary language="ja" />
    </MemoryRouter>,
  );
  fireEvent.change(screen.getByRole('searchbox'), { target: { value: word.text } });
  expect(screen.getAllByRole('article')).toHaveLength(1);
  fireEvent.click(screen.getByRole('button', { name: /Practice 10 words/ }));
  fireEvent.click(screen.getByRole('radio', { name: word.meaning.en }));
  fireEvent.click(screen.getByRole('button', { name: 'Check & save' }));
  fireEvent.click(await screen.findByRole('button', { name: 'View results →' }));
  expect(screen.getByRole('heading', { name: 'Session complete' })).toBeInTheDocument();
  expect(screen.getByText('You answered 1/1 words correctly.')).toBeInTheDocument();
  view.unmount();
  render(
    <MemoryRouter>
      <LanguageVocabulary language="ja" />
    </MemoryRouter>,
  );
  expect(await screen.findByText('Practiced')).toBeInTheDocument();
  expect(await db.attempts.count()).toBe(1);
});
