import { jwtDecode } from "jwt-decode";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("token");
  if (to.path === "/persons" && token.value) {
    try {
      const userState = useStateUser();
      userState.value = jwtDecode(token.value) as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
});
