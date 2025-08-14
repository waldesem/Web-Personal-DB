import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
  },
  app: {
    head: {
      htmlAttrs: { lang: "ru" },
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
      meta: [
        { name: "description", content: "Кадровая безопасность" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
      title: "StaffSec - кадровая безопасность",
    },
    keepalive: { include: "persons", max: 3 },
    pageTransition: { name: "page", mode: "out-in" },
  },
  build: {
    analyze: true,
  },
  compatibilityDate: "2025-07-05",
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
  },
  routeRules: {
    "/route/**": { proxy: "http://127.0.0.1:5000/route/**" },
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
