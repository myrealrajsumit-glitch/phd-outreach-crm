import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: parseInt(process.env.PORT || '5566', 10),
    strictPort: true,
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${process.env.BACKEND_PORT || '5555'}`,
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
