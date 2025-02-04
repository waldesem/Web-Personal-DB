import type { NitroFetchOptions } from "nitropack";
import { useStorageAsync, type RemovableRef } from "@vueuse/core";
import type { Token, Method } from "@/types";

export const accessToken = useStorageAsync("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const stateUser = useStorageAsync("stateUser", {}) as RemovableRef<Token>;

export const useFetchAuth = () => {
  const fetchAuth = async (
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
  return fetchAuth;
};
