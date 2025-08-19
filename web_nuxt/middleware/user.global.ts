import { useJwt } from "@vueuse/integrations/useJwt";
import type { Token } from "@/types";

// Создаем Middleware для получения данных пользователя
export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("token");
  if (token.value && to.path !== "/" && to.path !== "/login") {
    try {
      const userState = useStateUser();
      userState.value = useJwt(token.value).payload.value as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  }
});
