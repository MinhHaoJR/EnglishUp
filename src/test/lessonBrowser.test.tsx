import { render, screen, fireEvent, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import { db, defaults, resetData, logAttempt } from '../services/storage';
import Listening from '../features/listening/Listening';
import { listenings } from '../data/content';
import { byLevel } from '../components/LessonBrowser';

beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en' },
    level: 'all',
    topic: 'all',
    ready: true,
  });
});

test('the lesson list marks done lessons, counts them per level and offers the next one', async () => {
  const [first, second] = byLevel(listenings);
  await logAttempt('listening', 75, Date.now(), first.title);
  render(
    <MemoryRouter>
      <Listening />
    </MemoryRouter>,
  );
  const band = screen.getByRole('navigation', { name: 'Choose a level' });
  const levelButton = within(band).getByRole('button', { name: new RegExp(`^${first.level}`) });
  expect(await within(levelButton).findByText(/^1\//)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: `Next lesson: ${second.title}` })).toBeInTheDocument();
  expect(screen.getByRole('heading', { name: first.title }).closest('article')).toHaveTextContent(
    '75%',
  );

  fireEvent.click(screen.getByRole('checkbox', { name: 'Not done yet' }));
  expect(screen.queryByRole('heading', { name: first.title })).not.toBeInTheDocument();

  fireEvent.click(levelButton);
  expect(useApp.getState().level).toBe(first.level);
  expect(await db.attempts.count()).toBe(1);
});
