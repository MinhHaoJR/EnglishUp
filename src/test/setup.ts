import '@testing-library/jest-dom/vitest';
import 'fake-indexeddb/auto';
import { cleanup } from '@testing-library/react';
import { applyContent } from '../services/content';
import { seedRows } from '../data/seed';
afterEach(cleanup);
// The app downloads the library from the server; tests start with the seed lessons already loaded.
applyContent(seedRows);
