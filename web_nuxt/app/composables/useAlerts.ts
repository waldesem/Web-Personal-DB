import type { AlertProps } from "@nuxt/ui";

export function useAlert() {
  const alert = ref({
    icon: "i-lucide-circle-alert",
    color: "success",
    title: "Информация",
    description: "Введите логин и пароль",
  }) as Ref<AlertProps>;

  function setAlert(
    icon: string,
    color: string,
    title: string,
    description: string,
  ) {
    alert.value = {
      icon,
      color,
      title,
      description,
    };
  }

  return { alert, setAlert };
}
