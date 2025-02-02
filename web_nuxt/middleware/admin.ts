export default defineNuxtRouteMiddleware((_to) => {
  if (stateUser.value.role != "admin") {
    return navigateTo("/login");
  }
});