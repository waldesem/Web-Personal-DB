import type { AlertProps } from "@nuxt/ui";

export const useAlertStore = defineStore("alert", () => {
  const alert = ref({
    color: "success",
    title: "Информация",
    description: "Введите логин и пароль",
  }) as Ref<AlertProps>;

  function setAlert(color: string, title: string, description: string) {
    alert.value = {
      color,
      title,
      description,
    };
  }

  return { alert, setAlert };
});
