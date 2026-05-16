import type { FormField, Items } from "@/types";
import { Conclusions, Decisions } from "@/types";

export const formFields = {
  addresses: [
    {
      element: "select",
      key: "view",
      label: "Вид адреса",
      items: ["Адрес регистрации", "Адрес проживания", "Другое"],
      attrs: { placeholder: "Выберите адрес", required: true },
    },
    {
      element: "textarea",
      key: "address",
      label: "Адрес",
      attrs: { placeholder: "Введите адрес", maxlength: 4096, required: true },
    },
  ],
  affilations: [
    {
      element: "input",
      key: "view",
      label: "Вид участия",
      attrs: { placeholder: "Вид участия", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "organization",
      label: "Организация",
      attrs: { placeholder: "Организация", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "inn",
      label: "ИНН",
      attrs: { placeholder: "Организация", pattern: "^\\d{10,12}$" },
    },
    {
      element: "textarea",
      key: "activity",
      label: "Деятельность",
      attrs: { placeholder: "Деятельность", maxlength: 4096 },
    },
  ],
  checks: [
    {
      element: "textarea",
      key: "workplace",
      label: "Проверка по местам работы",
      attrs: { placeholder: "Проверка по местам работы", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "document",
      label: "Проверка документов",
      attrs: { placeholder: "Проверка документов", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "debt",
      label: "Проверка задолженностей",
      attrs: { placeholder: "Проверка задолженностей", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "bankruptcy",
      label: "Проверка банкротства",
      attrs: { placeholder: "Проверка банкротства", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "bki",
      label: "Проверка Кредитной истории",
      attrs: { placeholder: "Проверка Кредитной истории", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "courts",
      label: "Проверка судебных дел",
      attrs: { placeholder: "Проверка судебных дел", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "affilation",
      label: "Проверка аффилированности",
      attrs: { placeholder: "Проверка аффилированности", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "terrorist",
      label: "Проверка в списке террористов",
      attrs: { placeholder: "Проверка в списке террористов", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "internet",
      label: "Проверка в открытых источниках",
      attrs: { placeholder: "Проверка в открытых источниках", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "cronos",
      label: "Проверка в Кронос",
      attrs: { placeholder: "Проверка в Кронос", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "addition",
      label: "Дополнительная информация",
      attrs: { placeholder: "Дополнительная информация", maxlength: 4096 },
    },
    {
      element: "textarea",
      key: "comment",
      label: "Комментарий",
      attrs: { placeholder: "Комментарий", maxlength: 4096 },
    },
    {
      element: "select",
      key: "conclusion",
      label: "Результат",
      items: Object.values(Conclusions),
      attrs: { placeholder: "Выберите результат", required: true },
    },
  ],
  contacts: [
    {
      element: "select",
      key: "view",
      label: "Вид контакта",
      items: ["Телефон", "Электронная почта", "Другое"],
      attrs: {
        placeholder: "Выберите контакт",
        maxlength: 255,
        required: true,
      },
    },
    {
      element: "input",
      key: "contact",
      label: "Контакт",
      attrs: { placeholder: "Контакт", maxlength: 255, required: true },
    },
  ],
  documents: [
    {
      element: "select",
      key: "view",
      label: "Вид документа",
      items: ["Паспорт", "Иностранный паспорт", "Другое"],
      attrs: { placeholder: "Выберите документ", required: true },
    },
    {
      element: "input",
      key: "series",
      label: "Серия",
      attrs: { placeholder: "Серия", maxlength: 16 },
    },
    {
      element: "input",
      key: "digits",
      label: "Номер",
      attrs: { placeholder: "Номер", maxlength: 16, required: true },
    },
    {
      element: "input",
      key: "agency",
      label: "Кем выдан",
      attrs: { placeholder: "Орган выдавший", maxlength: 255 },
    },
    {
      element: "input",
      key: "issue",
      label: "Дата выдачи",
      attrs: { type: "date", required: true },
    },
  ],
  educations: [
    {
      element: "select",
      key: "view",
      label: "Вид образования",
      items: [
        "Основное общее",
        "Среднее общее",
        "Среднее профессиональное",
        "Высшее",
        "Неоконченное высшее образование",
        "Другое образование",
      ],
      attrs: { placeholder: "Выберите образование", required: true },
    },
    {
      element: "input",
      key: "institution",
      label: "Учебное заведение",
      attrs: {
        placeholder: "Учебное заведение",
        maxlength: 255,
        required: true,
      },
    },
    {
      element: "input",
      key: "finished",
      label: "Год окончания",
      attrs: { placeholder: "Год окончания", pattern: "^\\d{4}$" },
    },
    {
      element: "input",
      key: "specialty",
      label: "Специальность",
      attrs: { placeholder: "Специальность", maxlength: 255, required: true },
    },
  ],
  inquiries: [
    {
      element: "textarea",
      key: "info",
      label: "Информация",
      attrs: { placeholder: "Информация", maxlength: 4096, required: true },
    },
    {
      element: "input",
      key: "initiator",
      label: "Инициатор",
      attrs: { placeholder: "Инициатор", maxlength: 255, required: true },
    },
  ],
  investigations: [
    {
      element: "input",
      key: "theme",
      label: "Тема проверки",
      attrs: { placeholder: "Тема проверки", maxlength: 255, required: true },
    },
    {
      element: "textarea",
      key: "info",
      label: "Информация",
      attrs: { placeholder: "Информация", maxlength: 4096, required: true },
    },
  ],
  poligrafs: [
    {
      element: "select",
      key: "theme",
      label: "Тема проверки",
      items: [
        "Проверка кандидата",
        "Служебная проверка",
        "Служебное расследование",
        "Плановое мероприятие",
      ],
      attrs: { placeholder: "Выберите тему", required: true },
    },
    {
      element: "textarea",
      key: "results",
      label: "Результат",
      attrs: { placeholder: "Результат", maxlength: 4096, required: true },
    },
    {
      element: "select",
      key: "conclusion",
      label: "Результат",
      items: Object.values(Decisions),
      attrs: { placeholder: "Выберите результат", required: true },
    },
  ],
  previous: [
    {
      element: "input",
      key: "surname",
      label: "Фамилия",
      attrs: { placeholder: "Фамилия", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "firstname",
      label: "Имя",
      attrs: { placeholder: "Имя", maxlength: 255 },
    },
    {
      element: "input",
      key: "patronymic",
      label: "Отчество",
      attrs: { placeholder: "Отчество", maxlength: 255 },
    },
    {
      element: "input",
      key: "changed",
      label: "Год изменения",
      attrs: { placeholder: "Год изменения", pattern: "^\\d{4}$" },
    },
    {
      element: "textarea",
      key: "reason",
      label: "Причина",
      attrs: { placeholder: "Причина изменения", maxlength: 4096 },
    },
  ],
  staffs: [
    {
      element: "input",
      key: "position",
      label: "Должность",
      attrs: { placeholder: "Должность", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "department",
      label: "Подразделение",
      attrs: { placeholder: "Подразделение", maxlength: 255 },
    },
  ],
  workplaces: [
    {
      element: "input",
      key: "starts",
      label: "Начало работы",
      attrs: { type: "date", required: true },
    },
    {
      element: "input",
      key: "finished",
      label: "Окончание работы",
      attrs: { type: "date" },
    },
    {
      element: "input",
      key: "workplace",
      label: "Место работы",
      attrs: { placeholder: "Место работы", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "position",
      label: "Должность",
      attrs: { placeholder: "Должность", maxlength: 255, required: true },
    },
    {
      element: "input",
      key: "address",
      label: "Адрес организации",
      attrs: { placeholder: "Адрес организации", maxlength: 255 },
    },
    {
      element: "textarea",
      key: "reason",
      label: "Причина увольнения",
      attrs: { placeholder: "Причина увольнения", maxlength: 4096 },
    },
  ],
} as { [key in keyof Items]: FormField[] };
