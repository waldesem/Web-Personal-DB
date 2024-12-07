import type { NitroFetchOptions } from "nitropack";
import { getPayload } from "@/utils";
import type { Method } from "@/types";

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    const access = getPayload(accessToken.value);
    if (
      !accessToken.value ||
      (accessToken.value && access.exp < Date.now() / 1000)
    ) {
      if (!refreshToken.value) {
        return navigateTo("/login");
      } else {
        const refresh = getPayload(refreshToken.value);
        if (refresh.exp < Date.now() / 1000) {
          return navigateTo("/login");
        } else {
          const { access_token } = (await $fetch("/route/auth/refresh", {
            method: "GET",
            Authorization: `${refreshToken.value}`,
          })) as {
            access_token: string;
          };
          accessToken.value = access_token;
        }
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
