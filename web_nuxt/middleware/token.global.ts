import { jwtDecode } from "jwt-decode";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware(async (to) => {
  if (to.path !== "/login") {
    try {
      user.value = jwtDecode(accessToken.value.split(" ")[1]) as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
});
