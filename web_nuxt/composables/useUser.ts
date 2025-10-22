import type { Session } from "@/types";
import { useStorage } from "@vueuse/core";

// Создаем стейт для хранения данных пользователя
export const userState = useStorage("user", {} as Session, localStorage, {
  mergeDefaults: true,
});
