// import { Buffer } from "buffer";
import type { NitroFetchOptions } from "nitropack";
import { useStorage, type RemovableRef } from "@vueuse/core";
import type { Token, Method } from "@/types";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const stateUser = useStorage("stateUser", {}) as RemovableRef<Token>;

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
      const response = await $fetch(url, options);
      return response;
    } catch (error) {
      console.error(error);
      emitMessage("error");
      return navigateTo("/login");
    }
  };
  return fetchAuth;
};
