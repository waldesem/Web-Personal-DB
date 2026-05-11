import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src/app", import.meta.url)),
  },
  app: {
    buildAssetsDir: "assets",
    head: {
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
      meta: [
        { name: "description", content: "Кадровая безопасность" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
      noscript: [{ textContent: "JavaScript is required" }],
      title: "StaffSec - кадровая безопасность",
    },
    keepalive: { include: "persons", max: 1 },
    pageTransition: { name: "page", mode: "out-in" },
  },
  build: {
    analyze: true,
  },
  compatibilityDate: "2026-05-08",
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },
  experimental: {
    payloadExtraction: true,
    viteEnvironmentApi: true,
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
  sourcemap: { client: true },
  ui: {
    fonts: false,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
});
