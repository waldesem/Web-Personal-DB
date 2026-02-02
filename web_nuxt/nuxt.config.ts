import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src/app", import.meta.url)),
  },
  app: {
    keepalive: { include: "persons" },
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      title: "StaffSec - кадровая безопасность",
    },
  },
  build: {
    analyze: true,
  },
  compatibilityDate: "2026-01-31",
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },
  experimental: {
    entryImportMap: false,
  },
  icon: {
    clientBundle: {
      scan: true,
    },
  },
  modules: ["@nuxt/ui", "@nuxt/eslint", "@vueuse/nuxt", "nuxt-security"],
  nitro: {
    compressPublicAssets: { brotli: true },
  },
  routeRules: {
    "/routes/**": { proxy: "http://127.0.0.1:8000/routes/**" },
  },
  ui: {
    fonts: false,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
});
