import { useStorage } from "@vueuse/core";

export const userToken = useStorage("userToken", "", localStorage, {
  mergeDefaults: true,
});
