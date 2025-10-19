import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
  },
  app: {
    keepalive: { include: "persons", max: 2 },
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      title: "StaffSec - кадровая безопасность",
    },
  },
  build: {
    analyze: true,
  },
  compatibilityDate: "2025-10-05",
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },
  icon: {
    clientBundle: {
      scan: true,
    },
  },
  modules: ["@nuxt/ui", "@nuxt/eslint", "@vueuse/nuxt", "nuxt-security"],
  nitro: {
    output: {
      publicDir: "../server_flask/app/static",
    },
    prerender: {
      routes: ["/", "/users", "/persons", "/profile/[id]"],
    },
  },
  routeRules: {
    "/routes/**": { proxy: "http://127.0.0.1:5000/routes/**" },
  },
  ssr: false,
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
  ui: {
    colorMode: false,
  },
});
