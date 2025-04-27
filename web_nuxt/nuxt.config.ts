import { fileURLToPath } from "url";

export default defineNuxtConfig({
  compatibilityDate: "2024-03-16",
  devtools: { enabled: true },
  ssr: false,
  app: {
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      htmlAttrs: { lang: "ru" },
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
    },
  },
  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
  },
  routeRules: {
    "/route/**": { proxy: "http://127.0.0.1:5000/route/**" },
  },
  nitro: {
    output: {
      publicDir: "../server_flask/app/static",
    },
    minify: true,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
  modules: ["@nuxt/ui", "@nuxt/eslint", "@vueuse/nuxt"],
  css: ['~/assets/css/main.css'],
  icon: {
    clientBundle: {
      scan: true,
    },
  },
});
