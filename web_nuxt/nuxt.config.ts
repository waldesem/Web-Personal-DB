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
  compatibilityDate: "2026-03-28",
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },
  experimental: {
    //   entryImportMap: false,
    payloadExtraction: true,
  },
  icon: {
    clientBundle: {
      scan: true,
    },
  },
  modules: [
    "@nuxt/ui",
    "@nuxt/eslint",
    "@vueuse/nuxt",
    "nuxt-security",
    "@pinia/nuxt",
  ],
  nitro: {
    output: {
      publicDir: "../server_litestar_piccolo/app/static",
    },
  },
  routeRules: {
    "/routes/**": {
      proxy: "http://127.0.0.1:8000/routes/**",
    },
  },
  ssr: false,
  sourcemap: true,
  ui: {
    fonts: false,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
});
