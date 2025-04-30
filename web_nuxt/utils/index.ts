/**
 * Shows a toast message, depending on the value of the message parameter.
 * If message is "success", shows a green toast with title "Информация" and description "Информация обновлена".
 * Otherwise, shows a red toast with title "Внимание" and description "Ошибка обновления информации".
 *
 * @param message - "success" or any other value
 */
export function emitMessage(message: string) {
  const toast = useToast();
  if (message == "success") {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Успешно",
      description: "Информация обновлена",
      color: "success",
    });
  } else {
    toast.add({
      icon: "i-heroicons-exclamation-triangle",
      title: "Ошибка",
      description: "Невозможно выполнить действие",
      color: "error",
    });
  }
}