import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendPort = env.BACKEND_PORT || env.VITE_BACKEND_PORT || '8000'
  const frontendPort = parseInt(env.PORT || env.VITE_PORT || '5173', 10)

  return {
    plugins: [react()],
    server: {
      host: true,
      port: frontendPort,
      proxy: {
        '/api': {
          target: `http://127.0.0.1:${backendPort}`,
          changeOrigin: true,
          secure: false,
        }
      }
    }
  }
})
