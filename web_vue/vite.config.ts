import { defineConfig } from "vite";
import { fileURLToPath, URL } from "url";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: fileURLToPath(new URL("./src", import.meta.url)),
      },
      {
        find: "@components",
        replacement: fileURLToPath(
          new URL("./src/components", import.meta.url)
        ),
      },
    ],
  },
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000/api",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
        secure: false,
        ws: true,
      }
    }
  },
  build: {
    outDir: "../backend/app/static",
    emptyOutDir: true,
  },
});
