import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
export default defineConfig({
  plugins: [
    react(),
    // Installable app whose files are cached on first visit, so practice opens without a network.
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: 'auto',
      includeAssets: ['icons/apple-touch-icon.png', 'icons/favicon-64.png'],
      manifest: {
        name: 'EnglishUp',
        short_name: 'EnglishUp',
        description: 'Luyện tiếng Anh mỗi ngày, kể cả khi không có mạng.',
        lang: 'vi',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        background_color: '#f3f6f9',
        theme_color: '#0b5cad',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
          {
            src: '/icons/maskable-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,woff,woff2,png,svg}'],
        // The bundled vocabulary chunks are larger than Workbox's 2 MB default.
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
        navigateFallback: '/index.html',
        // API answers are personal and live: never serve them from the cache.
        navigateFallbackDenylist: [/^\/api\//],
      },
    }),
  ],
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
