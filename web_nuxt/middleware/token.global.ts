import { Buffer } from "buffer";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware((to) => {
  if (to.path === "/login") {
    return;
  }
  if (typeof(accessToken.value) !== "string") {
    return navigateTo("/login")
  };
  try {
    const token = accessToken.value.split(" ")[1];
    const payloads = token.split(".")[1];
    stateUser.value = JSON.parse(
      Buffer.from(payloads, "base64").toString()
    ) as Token;
    if (stateUser.value.exp < Date.now() / 1000) {
      return navigateTo("/login");
    }
  } catch (error) {
    console.error(error);
    return navigateTo("/login");
  }
});
