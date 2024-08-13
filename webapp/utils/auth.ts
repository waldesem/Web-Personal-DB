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

export const useFetchAuth = () => {
  const fetchAuth = async (
    url: string,
    options: NitroFetchOptions<ResponseType, Method> = {}
  ) => {
    const user_token = localStorage.getItem("user_token");
    if (user_token) {
      options.headers = {
        ...options.headers,
        Authorization: `Basic ${user_token}`,
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
