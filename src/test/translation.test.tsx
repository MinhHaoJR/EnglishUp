import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import TranslationPractice from '../features/vocabulary/TranslationPractice';
import { vocabulary, translations } from '../data/content';
import { useApp } from '../app/store';
import { db, defaults, resetData } from '../services/storage';

beforeEach(async () => {
  await resetData();
  useApp.setState({ settings: { ...defaults, language: 'en' }, level: 'A2', topic: 'Health' });
});
test.each(['vi-en', 'en-vi'] as const)(
  'word translation %s persists without changing SRS',
  async (direction) => {
    render(<TranslationPractice words={[vocabulary[0]]} />);
    fireEvent.change(screen.getByLabelText('Translation direction'), {
      target: { value: direction },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Start translating' }));
    expect(screen.getByRole('button', { name: 'Check answer' })).toBeDisabled();
    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: direction === 'vi-en' ? vocabulary[0].word : vocabulary[0].meaning },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
    expect(screen.getByText('Matches a reference answer!')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Save result and continue' }));
    await screen.findByRole('heading', { name: 'Session complete' });
    expect((await db.attempts.toArray())[0]).toMatchObject({ skill: 'vocabulary', score: 100 });
    expect(await db.reviews.count()).toBe(0);
  },
);
test.each(['vi-en', 'en-vi'] as const)(
  'sentence translation %s filters content and saves incorrect answers',
  async (direction) => {
    render(<TranslationPractice words={[]} />);
    fireEvent.change(screen.getByLabelText('Translation content'), {
      target: { value: 'sentence' },
    });
    fireEvent.change(screen.getByLabelText('Translation direction'), {
      target: { value: direction },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Start translating' }));
    const sentence = translations.find((item) => item.id === 'tr9')!;
    expect(
      screen.getByText(direction === 'vi-en' ? sentence.vi[0] : sentence.en[0]),
    ).toBeInTheDocument();
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'An unrelated answer' } });
    fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
    expect(screen.getByRole('textbox')).toHaveAttribute('readonly');
    fireEvent.click(screen.getByRole('button', { name: 'Save result and continue' }));
    await waitFor(async () => expect(await db.attempts.count()).toBe(1));
    expect((await db.attempts.toArray())[0].score).toBe(0);
  },
);
test('equivalent answers require explicit self-assessment and label the history', async () => {
  render(<TranslationPractice words={[vocabulary[0]]} />);
  fireEvent.click(screen.getByRole('button', { name: 'Start translating' }));
  fireEvent.change(screen.getByRole('textbox'), { target: { value: 'alternative translation' } });
  fireEvent.click(screen.getByRole('button', { name: 'Check answer' }));
  fireEvent.click(screen.getByRole('checkbox'));
  fireEvent.click(screen.getByRole('button', { name: 'Save result and continue' }));
  await waitFor(async () => expect(await db.attempts.count()).toBe(1));
  expect((await db.attempts.toArray())[0]).toMatchObject({
    score: 100,
    label: expect.stringContaining('self-assessed'),
  });
});
