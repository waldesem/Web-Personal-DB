import type { NitroFetchOptions } from "nitropack";
import { useStorage } from "@vueuse/core";
import type { Method } from "@/types";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const fetchAuth = async (
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
    await navigateTo("/login");
  }
};
