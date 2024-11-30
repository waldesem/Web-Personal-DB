import type { NitroFetchOptions } from "nitropack";

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
    if (accessToken.value) {
      options.headers = {
        ...options.headers,
        Authorization: `${accessToken.value}`,
      };
    } else {
      return navigateTo("/login");
    }
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
