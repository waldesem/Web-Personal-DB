import type { ToastProps } from "@nuxt/ui";

// Функция для отображения уведомлений в зависимости от статуса
export function useToasts() {
  const icon = {
    error: "i-lucide-triangle-alert",
    info: "i-lucide-octagon-alert",
    success: "i-lucide-circle-alert",
  };
  const title = {
    error: "Ошибка",
    info: "Внимание",
    success: "Успех",
  };
  const toast = useToast();
  function create(
    color: ToastProps["color"] = "error",
    description = "Невозможно выполнить действие или операция завершилась ошибкой"
  ) {
    toast.add({
      icon: icon[color as keyof typeof icon],
      title: title[color as keyof typeof title],
      description: description,
      color: color,
    });
  }
  return { create };
}
