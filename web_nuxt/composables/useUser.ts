import type { Token } from "@/types";
import { useJwt } from "@vueuse/integrations/useJwt";

// Создаем стейт для хранения данных пользователя
// export const useStateUser = () =>
//   useState("user", () => shallowRef({} as Token));

export const useStateUser = () =>
  useState("user", () => useJwt(useCookie("token")).payload.value as Token);
