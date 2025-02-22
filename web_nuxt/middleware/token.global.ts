import { useJwt } from "@vueuse/integrations/useJwt";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware((to) => {
  if (to.path !== "/login") {
    if (!accessToken.value) {
      return navigateTo("/login");
    }
    try {
      const bearer = accessToken.value.split(" ")[1];
      const { payload } = useJwt(bearer);
      stateUser.value = payload.value as Token;
      if (stateUser.value.exp < Date.now() / 1000) {
        accessToken.value = "";
        return navigateTo("/login");
      }
    } catch (error) {
      console.log(error);
      return navigateTo("/login");
    }
  }
});
