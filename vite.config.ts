import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
    host: true,
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          const normalized = id.replace(/\\/g, '/');
          if (normalized.includes('node_modules/lucide-react')) {
            return 'lucide';
          }
          if (normalized.includes('node_modules/')) {
            return 'vendor';
          }
          if (
            normalized.includes('/src/components/admin/') ||
            normalized.includes('/src/components/design-system/')
          ) {
            return 'admin-design';
          }
          if (
            normalized.includes('/src/components/booking/') ||
            normalized.includes('/src/components/field/') ||
            normalized.includes('/src/utils/qrCodeGenerator')
          ) {
            return 'booking-field';
          }
          if (
            normalized.includes('/src/components/map/') ||
            normalized.includes('/src/components/trails/') ||
            normalized.includes('/src/components/biodiversity/')
          ) {
            return 'topo-biodiversity';
          }
        },
      },
    },
  },
});
