import { useStorage } from "@vueuse/core";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const refreshToken = useStorage("refreshToken", "", localStorage, {
  mergeDefaults: true,
});
