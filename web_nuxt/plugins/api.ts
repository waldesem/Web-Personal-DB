import type { $Fetch, NitroFetchRequest } from "nitropack";

declare module "nuxt/app" {
  interface NuxtApp {
    $api: $Fetch<unknown, NitroFetchRequest>;
  }
}

export default defineNuxtPlugin(async (nuxtApp) => {
  const api = $fetch.create({
    async onRequest({ options }) {
      const token = useCookie("token", {
        maxAge: 60 * 58,
      });
      const refresh = useCookie("refresh");
      if (!refresh.value) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
      if (!token.value) {
        try {
          const { access_token } = (await $fetch("/route/auth/refresh", {
            headers: {
              Authorization: "Bearer " + refresh.value,
            },
            method: "POST",
          })) as { access_token: string };
          if (access_token) {
            token.value = access_token.split(" ")[1];
          } else {
            await nuxtApp.runWithContext(() => navigateTo("/login"));
          }
        } catch (error) {
          console.error(error);
          await nuxtApp.runWithContext(() => navigateTo("/login"));
        }
      }
      options.headers.set("Authorization", `Bearer ${token.value}`);
    },
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
    },
  });
  return { provide: { api } };
});
