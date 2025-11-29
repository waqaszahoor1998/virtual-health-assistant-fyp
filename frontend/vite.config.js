/**
 * Vite configuration file.
 * 
 * Vite is a fast build tool for modern web development.
 * This config sets up React plugin and development server settings.
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  // React plugin for JSX support and Fast Refresh
  plugins: [react()],
  
  // Development server configuration
  server: {
    port: 3000,  // Frontend dev server port
    proxy: {
      // Proxy API requests to backend server
      '/api': {
        target: 'http://localhost:5000',  // Backend server URL
        changeOrigin: true,
        secure: false,
      }
    }
  },
  
  // Build configuration
  build: {
    outDir: 'dist',  // Output directory for production build
    sourcemap: true,  // Generate source maps for debugging
  },
  
  // Path resolution
  resolve: {
    alias: {
      '@': '/src',  // Alias for src directory
    }
  }
})

