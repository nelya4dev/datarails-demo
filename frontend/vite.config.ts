import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // React core - rarely changes, good for long-term caching
          'react-core': ['react', 'react-dom', 'react/jsx-runtime'],

          // Routing and state management - moderate change frequency
          'react-vendor': [
            'react-router-dom',
            '@tanstack/react-query',
          ],

          // UI component library - rarely changes
          'radix-ui': [
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-progress',
            '@radix-ui/react-select',
            '@radix-ui/react-slot',
          ],

          // Utilities and icons
          'utils': [
            'clsx',
            'tailwind-merge',
            'class-variance-authority',
            'lucide-react',
          ],

          // Data table library
          'table': ['@tanstack/react-table'],

          // HTTP client and form handling
          'http': ['axios', 'react-dropzone'],
        },
      },
    },
    // Increase chunk size warning limit (we've optimized splitting)
    chunkSizeWarningLimit: 600,
  },
})
