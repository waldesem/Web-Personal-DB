import type { NitroFetchOptions } from "nitropack";
import { userToken, stateAlert} from "@/state/state";

const alertState = stateAlert();

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
      return navigateTo("/login");
    }

    try {
      const response = await $fetch(url, options);
      return response;
    } catch (error) {
      alertState.setAlert("rose", "Внимание", "Произошла ошибка");
      return Promise.reject(error);
    }
  };
  return fetchAuth;
};
