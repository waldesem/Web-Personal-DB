import { fileURLToPath } from "url";

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },
  ssr: false,
  app: {
    head: {
      htmlAttrs: { lang: "ru" },
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { charset: "utf-8" },
      ],
      style: [
        {
          children: "html, body { scrollbar-gutter: stable; }",
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
      publicDir: "../server_flask/app/static",
    }
  },

  vite: {
    build: {
      emptyOutDir: true,
    }
  },

  modules: [
    "@nuxt/image",
    "@nuxt/ui",
    "@nuxt/eslint",
    "@nuxtjs/color-mode",
    'nuxt-purgecss'
  ],
});