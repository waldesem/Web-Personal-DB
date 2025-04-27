import type { NitroFetchOptions } from "nitropack";
import { useStorageAsync } from "@vueuse/core";
import type { Method, Token } from "@/types";

export const accessToken = useStorageAsync("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const stateUser = ref({} as Token);

export const useFetchAuth = async (
  url: string,
  options: NitroFetchOptions<ResponseType, Method> = {}
) => {
  options.headers = {
    ...options.headers,
    Authorization: `${accessToken.value}`,
  };
  try {
    return await $fetch(url, options);
  } catch (error) {
    console.error(error);
    return navigateTo("/login");
  }
};
