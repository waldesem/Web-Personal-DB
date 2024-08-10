import { fileURLToPath } from "url";

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  app: {
    head: {
      htmlAttrs: { lang: "ru" },
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
      style: [
        {
          children: "body { scrollbar-gutter: stable; }",
        },
      ],
      noscript: [
        {
          children: "An application doesn't work without JavaScript",
        },
      ]
    },
  },

  alias: {
    "@/": fileURLToPath(new URL("./src", import.meta.url)),
    "@/components": fileURLToPath(new URL("./components", import.meta.url)),
    "@/pages": fileURLToPath(new URL("./pages", import.meta.url)),
    "@/utils": fileURLToPath(new URL("./utils", import.meta.url)),
  },

  routeRules: {
    '/api/**': { proxy: 'http://127.0.0.1:5000/api/**' }
  },

  nitro: {
    compressPublicAssets: true,
    output: {
      publicDir: "../backend/app/static",
    }
  },

  vite: {
    build: {
      emptyOutDir: true,
    }
  },

  csurf: {
    https: false,
    methodsToProtect: ["POST"],
  },

  modules: [
    "@nuxt/image",
    "nuxt-purgecss",
    "nuxt-security",
    "nuxt-csurf",
    "@nuxt/ui",
    "@nuxt/eslint",
    "@nuxtjs/color-mode"
  ],
});