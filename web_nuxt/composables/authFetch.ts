import type { NitroFetchOptions } from "nitropack";
import type { User } from "@/types";
import type { Method } from "@/types";
import { Buffer } from "buffer";

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    if (!accessToken.value) {
      return navigateTo("/login");
    }
    const cridentials = accessToken.value.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        stateUser.value = JSON.parse(
          Buffer.from(payloads[1], "base64").toString()
        ) as User;
      }
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
      return navigateTo("/login");
    }
  };
  return fetchAuth;
};
