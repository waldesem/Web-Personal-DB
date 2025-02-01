import { Buffer } from "buffer";
import type { Token } from "@/types";

export default defineNuxtRouteMiddleware((to) => {
  if (to.path === "/login") {
    return;
  }
  try {
    const token = accessToken.value.split(" ")[1];
    const payloads = token.split(".")[1];
    stateUser.value = JSON.parse(
      Buffer.from(payloads, "base64").toString()
    ) as Token;
    if (stateUser.value.exp < Date.now() / 1000) {
      emitMessage("error");
      return navigateTo("/login");
    }
  } catch (error) {
    console.error(error);
    emitMessage("error");
    return navigateTo("/login");
  }
});
