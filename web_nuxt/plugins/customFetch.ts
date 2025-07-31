export default defineNuxtPlugin((nuxtApp) => {
  const token = useCookie("token");
  const customFetch = $fetch.create({
    async onRequest({ options }) {
      if (token.value) {
        options.headers.set("Authorization", `${token.value}`);
      } else {
        await nuxtApp.runWithContext(() => navigateTo("/login"))
      }
    },
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
    },
  });
  return { provide: { customFetch }};
});
