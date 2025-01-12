import { Buffer } from "buffer";
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
    try {
      const token = accessToken.value.split(" ")[1];
      const payloads = token.split(".")[1];
      stateUser.value = JSON.parse(
        Buffer.from(payloads, "base64").toString()
      ) as Token;
      if (stateUser.value.exp < Date.now() / 1000) return navigateTo("/login");
    } catch (error) {
      console.error(error);
      return navigateTo("/login");
    }
    options.headers = {
      ...options.headers,
      Authorization: `${accessToken.value}`,
    };
    try {
      const response = await $fetch(url, options);
      return response;
    } catch (error) {
      console.error(error);
    }
  };
  return fetchAuth;
};
