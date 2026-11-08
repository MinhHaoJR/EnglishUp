import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  // Same-origin /api keeps the browser free of CORS rules; run the ASP.NET Core API on 5080.
  server: {
    proxy: { '/api': 'http://localhost:5080' },
    // Visual Studio locks files under server/.vs, which crashes Vite's watcher; the client never imports server/.
    watch: { ignored: ['**/server/**'] },
  },
  preview: { proxy: { '/api': 'http://localhost:5080' } },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom', 'react-router-dom'],
          storage: ['dexie', 'zod'],
          englishItVocabulary: ['src/data/itVocabularyContent.ts'],
          englishVocabulary: ['src/data/vocabularyContent.ts'],
        },
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    restoreMocks: true,
    // Flows that render the 2,080-word library can pass 5 s on a busy machine.
    testTimeout: 15_000,
  },
});
