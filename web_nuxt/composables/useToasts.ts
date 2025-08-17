import type { ToastProps } from "@nuxt/ui";

// Функция для отображения уведомлений в зависимости от статуса
export function useToasts(
  color: ToastProps["color"] = "error",
  description = "Невозможно выполнить действие или операция завершилсь ошибкой"
) {
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
