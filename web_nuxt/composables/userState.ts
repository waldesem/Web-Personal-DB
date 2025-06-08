import { useStorage } from "@vueuse/core";

export const useUserState = () => useState("user", () => ({} as Token));

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});
