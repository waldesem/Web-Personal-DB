import { jwtDecode } from "jwt-decode";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware((to) => {
  if (to.path !== "/login") {
    try {
      stateUser.value = jwtDecode(accessToken.value.split(" ")[1]) as Token;
    } catch (error) {
      console.error(error);
      return navigateTo("/login");
    }
  }
});
