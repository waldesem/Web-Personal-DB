import type { Session } from "@/types";

// Создаем стейт для хранения данных пользователя
export const userState = useState("user", () => ({}) as Session);
