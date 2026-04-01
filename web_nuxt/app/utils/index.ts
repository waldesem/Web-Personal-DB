import type { AuthFormField } from "@nuxt/ui";
import type { Items } from "@/types";

export const login: AuthFormField[] = [
  {
    name: "username",
    label: "Имя пользователя",
    placeholder: "Имя пользователя",
    icon: "i-lucide-user",
    type: "text",
    required: true,
  },
  {
    name: "password",
    label: "Пароль",
    placeholder: "Пароль",
    icon: "i-lucide-lock",
    type: "password",
    required: true,
  },
];

export const update = login.concat([
  {
    name: "new_pswd",
    label: "Новый пароль",
    placeholder: "Новый пароль",
    icon: "i-lucide-lock",
    type: "password",
    required: true,
  },
  {
    name: "conf_pswd",
    label: "Подтверждение пароля",
    placeholder: "Подтверждение пароля",
    icon: "i-lucide-lock",
    type: "password",
    required: true,
  },
]);

// Определяем массив элементов табов
export const tabs = [
  {
    label: "Анкета",
    icon: "i-lucide-user",
    slot: "anketa" as const,
  },
  {
    label: "Проверки",
    icon: "i-lucide-shield-check",
    slot: "checks" as keyof Items,
  },
  {
    label: "Полиграф",
    icon: "i-lucide-heart-pulse",
    slot: "poligrafs" as keyof Items,
  },
  {
    label: "Расследования",
    icon: "i-lucide-hat-glasses",
    slot: "investigations" as keyof Items,
  },
  {
    label: "Запросы",
    icon: "i-lucide-file-question-mark",
    slot: "inquiries" as keyof Items,
  },
];

// Определяем массив элементов аккордеона
export const accordion = [
  {
    label: "Должности",
    icon: "i-lucide-workflow",
    slot: "staffs" as keyof Items,
  },
  {
    label: "Образование",
    icon: "i-lucide-graduation-cap",
    slot: "educations" as keyof Items,
  },
  {
    label: "Места работы",
    icon: "i-lucide-briefcase-business",
    slot: "workplaces" as keyof Items,
  },
  {
    label: "Документы",
    icon: "i-lucide-book-text",
    slot: "documents" as keyof Items,
  },
  {
    label: "Адреса",
    icon: "i-lucide-house",
    slot: "addresses" as keyof Items,
  },
  {
    label: "Контакты",
    icon: "i-lucide-phone-call",
    slot: "contacts" as keyof Items,
  },
  {
    label: "Изменения имени",
    icon: "i-lucide-file-pen-line",
    slot: "previous" as keyof Items,
  },
  {
    label: "Аффилированность",
    icon: "i-lucide-users-round",
    slot: "affilations" as keyof Items,
  },
];
