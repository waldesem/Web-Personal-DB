import type { ToastProps } from "@nuxt/ui";

const toast = useToast();

// Функция для отображения уведомлений в зависимости от статуса
export function useToasts(
  color: ToastProps["color"] = "error",
  description = "Невозможно выполнить действие или операция завершилась ошибкой"
) {
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
  toast.add({
    icon: icon[color as keyof typeof icon],
    title: title[color as keyof typeof title],
    description: description,
    color: color,
  });
}