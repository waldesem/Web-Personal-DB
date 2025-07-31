import type { Token } from "@/types";

export const useStateUser = () => useState("user", () => ({} as Token));
