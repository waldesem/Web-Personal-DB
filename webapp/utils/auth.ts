import type { NitroFetchOptions } from "nitropack";
import { userToken } from "@/state/state";

type Method =
  | "get"
  | "post"
  | "put"
  | "delete"
  | "patch"
  | "head"
  | "connect"
  | "options"
  | "trace";

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    if (userToken.value) {
      options.headers = {
        ...options.headers,
        Authorization: `Basic ${userToken.value}`,
      };
    } else {
      navigateTo("/login");
      return Promise.reject(new Error("Unauthorized"));
    }

    try {
      const response = await $fetch(url, options);
      return response;
    } catch (error) {
      return Promise.reject(error);
    }
  };

  return fetchAuth;
};
