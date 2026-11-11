import { fireEvent, render, screen } from '@testing-library/react';
import { useState } from 'react';
import { Questions } from '../components/Questions';
import { useApp } from '../app/store';
import { defaults } from '../services/storage';
import type { Question } from '../data/schema';

const questions: Question[] = [
  {
    id: 'q1',
    type: 'choice',
    prompt: 'Who is the gift for?',
    options: ['Her brother', 'Her sister'],
    answers: ['Her brother'],
    explanation: 'She says so.',
    evidence: 'a gift for my brother',
  },
  {
    id: 'q2',
    type: 'short',
    prompt: 'Where do they meet?',
    answers: ['the bookshop'],
    explanation: 'Outside the bookshop.',
    evidence: 'outside the bookshop',
  },
];

function Harness({ submitted }: { submitted: boolean }) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  return (
    <Questions
      questions={questions}
      answers={submitted ? { q1: 'Her sister', q2: 'the bookshop' } : answers}
      submitted={submitted}
      onChange={(id, value) => setAnswers({ ...answers, [id]: value })}
    />
  );
}

beforeEach(() => useApp.setState({ settings: { ...defaults, language: 'en' } }));

test('shows one question at a time and marks answered stations', () => {
  render(<Harness submitted={false} />);
  expect(screen.getByRole('group', { name: '1. Who is the gift for?' })).toBeInTheDocument();
  expect(screen.queryByRole('group', { name: '2. Where do they meet?' })).not.toBeInTheDocument();
  expect(screen.getByRole('button', { name: /Previous question/ })).toBeDisabled();

  fireEvent.click(screen.getByRole('radio', { name: 'Her brother' }));
  expect(screen.getByRole('button', { name: 'Question 1, answered' })).toHaveAttribute(
    'aria-current',
    'step',
  );
  expect(screen.getByText('1/2 answered')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: /Next question/ }));
  expect(screen.getByRole('group', { name: '2. Where do they meet?' })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /Next question/ })).toBeDisabled();
});

test('after checking, stations say which answers were right', () => {
  render(<Harness submitted />);
  expect(screen.getByRole('button', { name: 'Question 1, wrong' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Question 2, right' }));
  expect(screen.getByText(/Outside the bookshop/)).toBeInTheDocument();
});

test('the check button waits for every answer, then options show right and wrong', () => {
  let checked = 0;
  function Checked() {
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [submitted, setSubmitted] = useState(false);
    return (
      <Questions
        questions={questions}
        answers={answers}
        submitted={submitted}
        onChange={(id, value) => setAnswers({ ...answers, [id]: value })}
        onCheck={() => {
          checked++;
          setSubmitted(true);
        }}
      />
    );
  }
  render(<Checked />);
  const check = screen.getByRole('button', { name: 'Check answer' });
  expect(check).toBeDisabled();
  expect(screen.getByText('2 still to answer.')).toBeInTheDocument();
  fireEvent.click(screen.getByRole('radio', { name: 'Her sister' }));
  fireEvent.click(screen.getByRole('button', { name: /Next question/ }));
  fireEvent.change(screen.getByRole('textbox'), { target: { value: 'the bookshop' } });
  expect(check).toBeEnabled();
  fireEvent.click(check);
  expect(checked).toBe(1);
  expect(screen.queryByRole('button', { name: 'Check answer' })).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Question 1, wrong' }));
  expect(screen.getByRole('radio', { name: 'Her brother' }).closest('label')).toHaveClass('right');
  expect(screen.getByRole('radio', { name: 'Her sister' }).closest('label')).toHaveClass('wrong');
});
