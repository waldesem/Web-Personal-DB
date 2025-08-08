import type { $Fetch, NitroFetchRequest } from "nitropack";

declare module "nuxt/app" {
  interface NuxtApp {
    $api: $Fetch<unknown, NitroFetchRequest>;
  }
}

export default defineNuxtPlugin(async (nuxtApp) => {
  const token = useCookie("token");
  const api = $fetch.create({
    async onRequest({ options }) {
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
