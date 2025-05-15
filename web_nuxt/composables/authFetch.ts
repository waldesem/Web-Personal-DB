import type { NitroFetchOptions } from "nitropack";
import { useStorage } from "@vueuse/core";
import type { Method, Persons, Token } from "@/types";

export const accessToken = useStorage("accessToken", "", localStorage, {
  mergeDefaults: true,
});

const useX = () => useState('x')

export const useColor = () => useState<string>('color', () => 'pink')

export const useFoo = () => {
  return useState('foo', () => 'bar')
}

export const user = ref({} as Token);

export const person = ref({} as Persons);

export const editable = computed(() => {
  return (
    person.value.editable &&
    user.value.role == "user" &&
    user.value.id == person.value.user_id
  );
});

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
