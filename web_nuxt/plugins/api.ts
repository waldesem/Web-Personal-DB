import type { $Fetch, NitroFetchRequest } from "nitropack";

declare module "nuxt/app" {
  interface NuxtApp {
    $api: $Fetch<unknown, NitroFetchRequest>;
  }
}

// Создаем плагин для работы с API
export default defineNuxtPlugin(async (nuxtApp) => {
  const api = $fetch.create({
    async onRequest({ options }) {
      const token = useCookie("token");
      options.headers.set("Authorization", `Bearer ${token.value}`);
    },

    // Обработка ошибок
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() =>
          navigateTo("/login")
        );
      }
    },
  });
  return { provide: { api } };
});
