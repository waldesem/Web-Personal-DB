import type { NitroFetchOptions } from "nitropack";
import { useStorageAsync } from "@vueuse/core";
import type { Method, Persons, Token } from "@/types";

export const accessToken = useStorageAsync("accessToken", "", localStorage, {
  mergeDefaults: true,
});

export const user = useState("user", () => ({} as Token));

export const person = useState("person", () => ({} as Persons));

export const editable = useState("editable", () =>
  computed(() => {
    return (
      person.value.editable &&
      user.value.role == "user" &&
      user.value.id == person.value.user_id
    );
  })
);

export const useFetchAuth = async (
  url: string,
  options: NitroFetchOptions<ResponseType, Method> = {}
) => {
  options.headers = {
    ...options.headers,
    Authorization: `${accessToken.value}`,
  };
  try {
    return await $fetch(url, options);
  } catch (error) {
    console.error(error);
    await navigateTo("/login");
  }
};
