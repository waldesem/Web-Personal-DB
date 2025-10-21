import type { Token } from "@/types";
import { useStorage } from "@vueuse/core";

// Создаем стейт для хранения данных пользователя
export const userState = useStorage("user", {} as Token, localStorage, {
  mergeDefaults: true,
});
