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
    console.log(cookies.value);
    if (userToken.value || cookies.value) {
      options.headers = {
        ...options.headers,
        Authorization: `${userToken.value}`,
        "x-h3-session": cookies.value || "",
      };
    } else {
      return navigateTo("/login");
    }
    // Add cookies to request headers if they exist
    if (cookies.value) {
      options.credentials = "include";
      options.headers = {
        ...options.headers,
        Cookie: `h3=${cookies.value}`,
      };
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
