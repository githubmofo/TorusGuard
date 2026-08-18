import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// TORUSGUARD-DEMO: Public source maps enabled in production
export default defineConfig({
  plugins: [react()],
  build: {
    sourcemap: true,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:3001',
    },
  },
});
