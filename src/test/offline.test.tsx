import { act, render, screen } from '@testing-library/react';
import { OfflineSign } from '../components/OfflineSign';
import { useApp } from '../app/store';
import { defaults } from '../services/storage';

const setOnline = (value: boolean) =>
  Object.defineProperty(window.navigator, 'onLine', { configurable: true, get: () => value });

beforeEach(() => useApp.setState({ settings: { ...defaults, language: 'vi' } }));
afterEach(() => setOnline(true));

test('shows the offline sign only while the connection is down', () => {
  setOnline(true);
  render(<OfflineSign />);
  expect(screen.queryByText('Đang offline')).not.toBeInTheDocument();

  act(() => {
    setOnline(false);
    window.dispatchEvent(new Event('offline'));
  });
  expect(screen.getByRole('status')).toHaveTextContent('Đang offline');

  act(() => {
    setOnline(true);
    window.dispatchEvent(new Event('online'));
  });
  expect(screen.queryByText('Đang offline')).not.toBeInTheDocument();
});
