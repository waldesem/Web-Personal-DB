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
      // Получаем токен доступа
      const token = useCookie("access", {
        maxAge: 60 * 59,
        sameSite: "strict",
        watch: "shallow",
      });

      // Если токен доступа не найден, получаем новый токен доступа из API
      if (!token.value) {
        // Получаем токен обновления
        const refresh = useCookie("refresh");
        // Если токен не найден, переходим на страницу логина
        if (!refresh.value) {
          await nuxtApp.runWithContext(() => navigateTo("/login"));
        }

        try {
          const res = await $fetch.raw("/routes/auth/refresh", {
            method: "GET",
            headers: {
              Authorization: refresh.value,
            },
          });
          token.value = res.headers?.get("Authorization");
        } catch (error) {
          console.error(error);
          await nuxtApp.runWithContext(() => navigateTo("/login"));
        }
      }

      // Если токен доступа найден, добавляем его в заголовок запроса
      options.headers.set("Authorization", token.value as string);
    },

    // Обработка ошибок
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
    },
  });
  return { provide: { api } };
});
