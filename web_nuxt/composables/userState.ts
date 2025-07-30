import type { Token } from "@/types";

export const stateUser = () => useState("user", () => ({} as Token));

export const accessToken = useCookie("token", {
  maxAge: 60 * 60 * 24, // 1 day
});
