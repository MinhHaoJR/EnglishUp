import '@testing-library/jest-dom/vitest';
import 'fake-indexeddb/auto';
import { cleanup, configure } from '@testing-library/react';
import { applyContent } from '../services/content';
import { seedRows } from '../data/seed';
afterEach(cleanup);
// With every file running in parallel, a save to IndexedDB can take more than the default second.
configure({ asyncUtilTimeout: 5000 });
// The app downloads the library from the server; tests start with the seed lessons already loaded.
applyContent(seedRows);
