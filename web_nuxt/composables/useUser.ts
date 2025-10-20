import type { Token } from "@/types";
import { useJwt } from "@vueuse/integrations/useJwt";

// Создаем стейт для хранения данных пользователя
export const useStateUser = () =>
  useState("user", () => {
    try {
      const token = useCookie("token");
      if (token.value) {
        return useJwt(token.value).payload.value as Token;
      } else {
        return {} as Token;
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(error);
      }
      return {} as Token;
    }
  });
