import { fileURLToPath } from "url";

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },

  app: {
    head: {
      title: "StaffSec",
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
      style: [
        {
          children: "body { scrollbar-gutter: stable; }",
        },
      ],
      script: [
        {
          src: "/js/bootstrap.bundle.min.js",
        },
      ],
      noscript: [
        {
          children: "An application doesn't work without JavaScript",
        },
      ]
    },
  },

  css: [
    "bootstrap/dist/css/bootstrap.min.css",
    "bootstrap-icons/font/bootstrap-icons.min.css",
  ],

  nitro: {
    output: {
      publicDir: "../backend/app/static",
    }
  },

  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
    "@/components": fileURLToPath(new URL("./components", import.meta.url)),
    "@/pages": fileURLToPath(new URL("./pages", import.meta.url)),
    "@/utils": fileURLToPath(new URL("./utils", import.meta.url)),
  },

  vite: {
    build: {
      emptyOutDir: true,
    }
  },

  modules: ["@nuxt/image"]
});