import { defineConfig } from 'vite'
import { fileURLToPath, URL } from "url";
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      { find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) },
      { find: '@store', replacement: fileURLToPath(new URL('./src/store', import.meta.url)) },
      { find: '@router', replacement: fileURLToPath(new URL('./src/router', import.meta.url)) },
      { find: '@components', replacement: fileURLToPath(new URL('./src/components', import.meta.url)) },
      { find: '@layouts', replacement: fileURLToPath(new URL('./src/components/layouts', import.meta.url)) },
      { find: '@pages', replacement: fileURLToPath(new URL('./src/components/pages', import.meta.url)) },
      { find: '@content', replacement: fileURLToPath(new URL('./src/components/content', import.meta.url)) },
    ],
  },
  build: {
    outDir: '../backend/app/static',
  }
})
