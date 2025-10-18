import { useJwt } from "@vueuse/integrations/useJwt";
import type { Token } from "@/types";

// Создаем Middleware для получения данных пользователя
export default defineNuxtRouteMiddleware(async () => {
  const token = useCookie("token");
  if (token.value) {
    try {
      const userState = useStateUser();
      userState.value = useJwt(token.value).payload.value as Token;
    } catch (error) {
      console.error(error);
      await navigateTo("/login");
    }
  } else {
    const refresh = useCookie("refresh");
    if (refresh.value) {
      try {
        // Запрашиваем новый токен доступа с помощью токена обновления
        const access_token = await refreshToken(refresh.value);
        if (access_token) {
          // Если токен доступа получен, сохраняем его в cookie
          token.value = access_token;
        } else {
          await navigateTo("/login");
        }
      } catch (error) {
        console.error(error);
        await navigateTo("/login");
      }
    } else {
      await navigateTo("/login");
    }
  }
});
