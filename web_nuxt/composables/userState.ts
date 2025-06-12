import { useStorage } from "@vueuse/core";
import type { Token } from "@/types";

export const useUserState = () => useState("user", () => shallowRef({} as Token));

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});
