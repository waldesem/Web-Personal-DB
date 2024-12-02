import type { NitroFetchOptions } from "nitropack";
import type { Token } from "@/types";
import type { Method } from "@/types";
import { Buffer } from "buffer";

function getPayload(token: string | null = accessToken.value) {
  if (token) {
    const cridentials = token.split(" ");
    if (cridentials.length > 1) {
      const payloads = cridentials[1].split(".");
      if (payloads.length > 1) {
        stateUser.value = JSON.parse(
          Buffer.from(payloads[1], "base64").toString()
        ) as Token;
      }
    }
  }
  return {} as Token;
}

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    getPayload();
    if (
      !accessToken.value ||
      (accessToken.value && stateUser.value.exp < Date.now() / 1000)
    ) {
      if (!refreshToken.value) {
        return navigateTo("/login");
      } else {
        getPayload(refreshToken.value);
        if (stateUser.value.exp < Date.now() / 1000) {
          return navigateTo("/login");
        } else {
          const { access_token } = (await $fetch("/api/refresh", {
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
