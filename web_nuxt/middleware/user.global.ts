import { jwtDecode } from "jwt-decode";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("token");
  if (token.value && to.path !== "/" && to.path !== "/login") {
    try {
      const userState = useStateUser();
      userState.value = jwtDecode(token.value) as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
});
