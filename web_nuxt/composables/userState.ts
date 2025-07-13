import { useStorage } from "@vueuse/core";
import type { Token } from "@/types";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const useUserState = () => useState("user", () => ({}) as Token);
