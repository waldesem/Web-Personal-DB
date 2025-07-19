export default defineNuxtPlugin((nuxtApp) => {
  const customFetch = $fetch.create({
    onRequest({ options }) {
      if (accessToken.value) {
        options.headers.set("Authorization", `${accessToken.value}`);
      }
    },
    async onResponseError({ response }) {
      if (response.status === 401 || response.status === 403) {
        await nuxtApp.runWithContext(() => navigateTo("/login"));
      }
    },
  });
  // Expose to useNuxtApp().$customFetch
  return { provide: { customFetch }};
});
