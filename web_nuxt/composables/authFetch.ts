import type { NitroFetchOptions } from "nitropack";
import { getPayload } from "@/utils";

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
    await checkAuthTokens();
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

async function checkAuthTokens() {
  const options = ref({} as NitroFetchOptions<ResponseType, Method>);
  const access = getPayload(accessToken.value);
  const refresh = getPayload(refreshToken.value);
  if (
    !accessToken.value ||
    (accessToken.value && access.exp < Date.now() / 1000)
  ) {
    if (!refreshToken.value) {
      return navigateTo("/login");
    } else {
      if (refresh.exp < Date.now() / 1000) {
        return navigateTo("/login");
      } else {
        options.value.headers = {
          ...options.value.headers,
          Authorization: `${refreshToken.value}`,
        };
        const { access_token } = (await $fetch(
          "/api/refresh",
          options.value
        )) as {
          access_token: string;
        };
        accessToken.value = access_token;
      }
    }
  }
}