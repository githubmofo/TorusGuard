import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// TG-CLIENT-001: Public production source maps enabled
export default defineConfig({
  plugins: [react()],
  build: { sourcemap: true },
  server: {
    port: 5173,
    proxy: { '/api': 'http://localhost:3001' },
  },
});
