import type { Token } from "@/types";

// Создаем стейт для хранения данных пользователя
export const useStateUser = () =>
  useState("user", () => shallowRef({} as Token));
