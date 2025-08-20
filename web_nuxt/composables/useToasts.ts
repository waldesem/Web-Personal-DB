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
}

/**
 * Класс для создания и отображения уведомлений (toast) с предопределенными стилями.
 */
class Toaster {
  /**
   * Символы иконок для разных типов уведомлений.
   * 
   * @property {string} error - Иконка для ошибок.
   * @property {string} info - Иконка для информационных сообщений.
   * @property {string} success - Иконка для успешных действий.
   */
  icon = {
    error: "i-heroicons-exclamation-triangle",
    info: "i-heroicons-exclamation-circle",
    success: "i-heroicons-information-circle",
  };

  /**
   * Заголовки для разных типов уведомлений.
   * 
   * @property {string} error - Заголовок для ошибок.
   * @property {string} info - Заголовок для информационных сообщений.
   * @property {string} success - Заголовок для успешных действий.
   */
  title = {
    error: "Ошибка",
    info: "Внимание",
    success: "Успех",
  };

  /**
   * Конструктор класса `Toaster`.
   * 
   * @param {("error" | "info" | "success")} color - Тип уведомления (цвет). По умолчанию: "error".
   * @param {string} description - Описание уведомления. По умолчанию: "Невозможно выполнить действие...".
   * 
   * Инициализирует экземпляр класса и сразу вызывает метод `createToast()` для отображения уведомления.
   */
  constructor(
    private color: "error" | "info" | "success" = "error",
    private description: string = "Невозможно выполнить действие..."
  ) {
    (this.color = color), (this.description = description), this.createToast();
  }

  /**
   * Создает и отображает уведомление (toast) на основе текущих настроек.
   * 
   * Использует метод `useToast()` для получения экземпляра уведомления и метод `add()` для его отображения.
   * Параметры уведомления:
   * - `icon`: Иконка, соответствующая типу (`this.color`).
   * - `title`: Заголовок, соответствующий типу (`this.color`).
   * - `description`: Описание уведомления.
   * - `color`: Цвет уведомления.
   */
  createToast() {
    const toast = useToast();
    toast.add({
      icon: this.icon[this.color],
      title: this.title[this.color],
      description: this.description,
      color: this.color,
    });
  }
}


export const useToaster = new Toaster();
