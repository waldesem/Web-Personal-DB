import type { AuthFormField } from "@nuxt/ui";
import type { Items, Login, Person } from "@/types";

export function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export const fieldsLogin: AuthFormField[] = [
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

export const fieldsUpdate = fieldsLogin.concat([
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
export const tabsItems = [
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
export const accordionItems = [
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

export const validatorLogin = (state: Partial<Login>) => {
  const errors = [];
  if (!state.username) {
    errors.push({
      name: "username",
      message: "Введите имя пользователя",
    });
  }
  if (!state.password) {
    errors.push({
      name: "password",
      message: "Введите пароль",
    });
  }
  return errors;
};

export const validatorUpdate = (state: Partial<Login>) => {
  const errors = validatorLogin(state);
  if (
    state.new_pswd &&
    !state.new_pswd.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/)
  ) {
    errors.push({
      name: "new_pswd",
      message: "От 8 до 16 цифр и латинских букв в нижнем и верхнем регистре",
    });
  }
  if (state.password === state.new_pswd) {
    errors.push({
      name: "new_pswd",
      message: "Старый и новый пароли совпадают",
    });
  }
  if (state.conf_pswd !== state.new_pswd) {
    errors.push({
      name: "conf_pswd",
      message: "Новый пароль и подтверждение не совпадают",
    });
  }
  return errors;
};

export const validatorResume = (state: Partial<Person>) => {
  const errors = [];
  if (!state.surname?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)) {
    errors.push({
      name: "surname",
      message: "Введите корректную фамилию",
    });
  }
  if (!state.firstname?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)) {
    errors.push({
      name: "firstname",
      message: "Введите корректное имя",
    });
  }
  if (
    state.patronymic &&
    !state.patronymic?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)
  ) {
    errors.push({
      name: "patronymic",
      message: "Введите корректное отчество",
    });
  }
  return errors;
};
