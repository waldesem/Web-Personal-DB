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
      // Получаем токен обновления
      const refresh = useCookie("refresh");
      // Если токен не найден, переходим на страницу логина
      if (!refresh.value) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
      // Получаем токен доступа
      const token = useCookie("token") ?? useCookie("token", {
        maxAge: 60 * 59,
        sameSite: 'strict',
        watch: "shallow",
      });
      // Если токен доступа не найден, получаем новый токен доступа из API
      if (!token.value) {
        try {
          // Запрашиваем новый токен доступа с помощью токена обновления
          const { access_token } = (await $fetch("/routes/auth/refresh", {
            headers: {
              Authorization: "Bearer " + refresh.value,
            },
            method: "POST",
          })) as { access_token: string };
          if (access_token) {
            // Если токен доступа получен, сохраняем его в cookie
            token.value = access_token.split(" ")[1];
          } else {
            await nuxtApp.runWithContext(() => navigateTo("/login"));
          }
        } catch (error) {
          console.error(error);
          await nuxtApp.runWithContext(() => navigateTo("/login"));
        }
      }
      // Если токен доступа найден, добавляем его в заголовок запроса
      options.headers.set("Authorization", `Bearer ${token.value}`);
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
