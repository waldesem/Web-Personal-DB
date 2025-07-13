import { useStorage } from "@vueuse/core";
import type { Token } from "@/types";
import { jwtDecode } from "jwt-decode";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const useUserState = () =>
  useState("user", () =>
    computed(() => jwtDecode(accessToken.value.split(" ")[1]) as Token)
  );
