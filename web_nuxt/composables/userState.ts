import type { Token } from "@/types";

export const useUserState = () => useState("user", () => ({} as Token));
