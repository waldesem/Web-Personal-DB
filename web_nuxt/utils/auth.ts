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

  /**
   * Returns a function that wraps `$fetch` and adds an Authorization header if a user token is present.
   *
   * @returns {(url: string, options?: NitroFetchOptions<ResponseType, Method>) => Promise<ResponseType>}
   */
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
      return navigateTo("/login");
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
