export default defineNuxtRouteMiddleware(async (to) => {
  if (to.path !== "/login" && to.path !== "/") {
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
            maxAge: 60 * 15,
          });
          token.value = access_token.split(" ")[1];
        } else {
          await navigateTo("/login");
        }
      } catch (error) {
        console.error(error);
        await navigateTo("/login");
      }
    }
  }
});
