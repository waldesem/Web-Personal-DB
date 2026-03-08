import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src/app", import.meta.url)),
  },
  app: {
    buildAssetsDir: "assets",
    keepalive: { include: "persons" },
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      title: "StaffSec - кадровая безопасность",
    },
  },
  build: {
    analyze: true,
  },
  compatibilityDate: "2026-03-08",
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
    output: {
      publicDir: "../server_litestar/app/static",
    },
  },
  routeRules: {
    "/routes/**": {
      proxy: "http://127.0.0.1:8000/routes/**",
    },
  },
  ssr: false,
  ui: {
    fonts: false,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
});
