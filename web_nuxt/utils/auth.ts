import type { NitroFetchOptions } from "nitropack";
import { Buffer } from "buffer";

export const userToken = ref("");

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
        Authorization: `${userToken.value}`,
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

export const stateUser = () => {
  if (!userToken.value) {
    return {} as Ref<User>;
  }
  const payload = userToken.value.split(" ")[1];
  const user = useState(
    "user",
    () =>
      JSON.parse(
        Buffer.from(payload.split(".")[1], "base64").toString()
      ) as User
  );
  return user as Ref<User>;
};
