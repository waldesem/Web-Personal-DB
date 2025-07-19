export default defineNuxtPlugin((nuxtApp) => {
  const api = $fetch.create({
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
  // Expose to useNuxtApp().$api
  return { provide: { api } };
});
