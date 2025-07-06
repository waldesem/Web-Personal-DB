import { jwtDecode } from "jwt-decode";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware(async (to) => {
  if (to.path !== "/login" && to.path !== "/") {
    try {
      const userState = useUserState();
      userState.value = jwtDecode(accessToken.value.split(" ")[1]) as Token;
      if (userState.value.exp < new Date().getTime() / 1000) {
        accessToken.value = null;
        return navigateTo("/login", { redirectCode: 301 });
      }
      return;
    } catch (error) {
      console.error(error);
      return navigateTo("/login", { redirectCode: 301 });
    }
  }
});
