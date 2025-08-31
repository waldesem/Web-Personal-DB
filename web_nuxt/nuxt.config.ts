import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
  },
  app: {
    keepalive: { include: "persons", max: 3 },
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      title: "StaffSec - кадровая безопасность",
    },
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
    // database: {
    //   default: {
    //     connector: "sqlite",
    //     options: {
    //       name: "database.db",
    //       path: "/home/semenenko/MyProjects/Web-Personal-DB/server_flask/PersonalDB/database.db",
    //     },
    //   },
    // },
    // experimental: {
    //   database: true,
    // },
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
