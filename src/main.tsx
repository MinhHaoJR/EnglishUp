import React from 'react';
import ReactDOM from 'react-dom/client';
const App = React.lazy(() => import('./app/App'));
import './styles.css';
import './styles/vibrant.css';
class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { error: boolean }> {
  state = { error: false };
  static getDerivedStateFromError() {
    return { error: true };
  }
  render() {
    return this.state.error ? (
      <main>
        <h1>EnglishUp</h1>
        <p role="alert">Không thể tải ứng dụng. / The app could not load.</p>
        <button onClick={() => location.reload()}>Tải lại / Reload</button>
      </main>
    ) : (
      this.props.children
    );
  }
}
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <React.Suspense
        fallback={
          <p className="notice" role="status">
            Đang tải / Loading…
          </p>
        }
      >
        <App />
      </React.Suspense>
    </ErrorBoundary>
  </React.StrictMode>,
);
