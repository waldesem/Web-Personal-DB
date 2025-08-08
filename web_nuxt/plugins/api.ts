import type { $Fetch, NitroFetchRequest } from "nitropack";

declare module "nuxt/app" {
  interface NuxtApp {
    $api: $Fetch<unknown, NitroFetchRequest>;
  }
}

export default defineNuxtPlugin(async (nuxtApp) => {
  const token = useCookie("token");
  const refresh = useCookie("refresh");
  if (!refresh.value) {
    await navigateTo("/login");
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
        const token = useCookie("token", {
          maxAge: 60 * 60 * 12,
        });
        token.value = access_token;
      } else {
        await navigateTo("/login");
      }
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
  const api = $fetch.create({
    async onRequest({ options }) {
      options.headers.set("Authorization", `Bearer ${token.value}`);
    },
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      } else if (response.status === 404) {
        await nuxtApp.runWithContext(() => navigateTo("/error"));
      }
    },
  });
  return { provide: { api } };
});
