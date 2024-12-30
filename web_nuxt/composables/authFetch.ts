import { Buffer } from "buffer";
import type { NitroFetchOptions } from "nitropack";
import type { Token, Method } from "@/types";
import { z } from "zod";

const token = z.string().jwt({"alg": "HS256"});

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    try {
      token.parse(accessToken.value);
      const payloads = accessToken.value.split(" ")[1].split(".")[1];
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
      return navigateTo("/login");
    }
  };
  return fetchAuth;
};
