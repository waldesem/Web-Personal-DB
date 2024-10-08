export default defineNuxtRouteMiddleware(to => {
  if (to.path != "/login") {
    if (!userToken.value) {
      return navigateTo("/login")
    };
  } else {
    reloadNuxtApp()
  };
});
