import type { NitroFetchOptions } from "nitropack";
import type { ToastProps } from "@nuxt/ui";

export const fetchAuth = async (
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

export const makeToast = (
  color: ToastProps["color"] = "error",
  description = "Невозможно выполнить действие или операция завершилсь ошибкой"
) => {
  const icon = {
    error: "i-heroicons-exclamation-triangle",
    info: "i-heroicons-exclamation-circle",
    success: "i-heroicons-information-circle",
  };
  const title = {
    error: "Ошибка",
    info: "Внимание",
    success: "Успех",
  };
  const toast = useToast();
  toast.add({
    icon: icon[color as keyof typeof icon],
    title: title[color as keyof typeof title],
    description: description,
    color: color,
  });
};
