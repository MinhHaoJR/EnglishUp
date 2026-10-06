import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useApp } from '../app/store';
import LanguagePicker from '../features/languages/LanguagePicker';
import LanguageWorkspace from '../features/languages/LanguageWorkspace';
import Dashboard from '../features/dashboard/Dashboard';
import { db, defaults, exportData, importData, resetData, logAttempt } from '../services/storage';
import { languageLessons } from '../data/languages';
import { skills } from '../services/progress';
import { matchesModel } from '../services/languages';
beforeEach(async () => {
  await resetData();
  useApp.setState({
    settings: { ...defaults, language: 'en', learningLanguage: 'ja' },
    ready: true,
  });
});
function show(element: React.ReactNode) {
  return render(<MemoryRouter>{element}</MemoryRouter>);
}
test('picker persists target language independently of interface language and reloads it', async () => {
  show(<LanguagePicker />);
  fireEvent.change(screen.getByLabelText('Learning language'), { target: { value: 'zh' } });
  await waitFor(async () => expect((await db.settings.get('main'))?.learningLanguage).toBe('zh'));
  await useApp.getState().load();
  expect(useApp.getState().settings).toMatchObject({ language: 'en', learningLanguage: 'zh' });
});
for (const language of ['ja', 'zh'] as const) {
  for (const skill of skills) {
    test(`${language} ${skill} completes and persists its own attempt`, async () => {
      useApp.setState({ settings: { ...defaults, language: 'en', learningLanguage: language } });
      show(<LanguageWorkspace skill={skill} />);
      fireEvent.click(screen.getAllByRole('button', { name: 'Start practice' })[0]);
      const lesson = languageLessons.find((item) => item.language === language)!;
      if (skill === 'reading' || skill === 'vocabulary')
        fireEvent.click(screen.getAllByRole('radio')[0]);
      else if (skill === 'speaking') fireEvent.click(screen.getByRole('checkbox'));
      else fireEvent.change(screen.getByRole('textbox'), { target: { value: lesson.text } });
      fireEvent.click(screen.getByRole('button', { name: 'Finish & save' }));
      await screen.findByText(/Practice saved/);
      const attempts = await db.attempts.toArray();
      expect(attempts).toHaveLength(1);
      expect(attempts[0]).toMatchObject({ skill, learningLanguage: language, score: 100 });
      if (skill === 'writing') expect(await db.submissions.count()).toBe(1);
    });
  }
}
test('Japanese history excludes Chinese and legacy English attempts', async () => {
  await logAttempt('reading', 100, Date.now(), 'Japanese result', 'ja');
  await logAttempt('reading', 100, Date.now(), 'Chinese result', 'zh');
  await db.attempts.add({
    id: 'old',
    skill: 'reading',
    score: 100,
    duration: 1,
    timestamp: Date.now(),
    label: 'Legacy English result',
  });
  const view = show(<LanguageWorkspace />);
  expect(await screen.findByText(/Japanese result/)).toBeInTheDocument();
  expect(screen.queryByText(/Chinese result/)).not.toBeInTheDocument();
  expect(screen.queryByText(/Legacy English result/)).not.toBeInTheDocument();
  view.unmount();
  show(<Dashboard />);
  expect(await screen.findByText('Legacy English result')).toBeInTheDocument();
  expect(screen.queryByText(/Japanese result/)).not.toBeInTheDocument();
});
test('backup restores language choice and results, accepts legacy settings and rejects invalid language atomically', async () => {
  await db.settings.put({ ...defaults, learningLanguage: 'zh' });
  await logAttempt('listening', 100, Date.now(), '你好', 'zh');
  const snapshot = await exportData();
  await resetData();
  await importData(snapshot);
  expect(await exportData()).toEqual(snapshot);
  await expect(
    importData({ ...snapshot, settings: { ...snapshot.settings, learningLanguage: 'invalid' } }),
  ).rejects.toThrow();
  expect(await exportData()).toEqual(snapshot);
  const { learningLanguage: omitted, ...legacy } = defaults;
  expect(omitted).toBe('en');
  await importData({ ...snapshot, settings: legacy });
  await useApp.getState().load();
  expect(useApp.getState().settings.learningLanguage).toBe('en');
});
test('script answers normalize width, punctuation and spaces without losing meaningful characters', () => {
  expect(matchesModel(' 你好！', '你好')).toBe(true);
  expect(matchesModel('水をください。', '水をください')).toBe(true);
  expect(matchesModel('您好', '你好')).toBe(false);
  expect(matchesModel('nǐ hǎo', '你好')).toBe(false);
});
