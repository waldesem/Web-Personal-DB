import { Conclusions, Decisions } from "@/types";
import type { Items, FormFields } from "@/types";

const pattern = "^[А-ЯЁ][А-ЯЁ\\-.,' ]+[А-ЯЁ]$";

export const person = [
  {
    key: "surname",
    label: "Фамилия",
    props: {
      pattern: pattern,
      placeholder: "Фамилия (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    key: "firstname",
    label: "Имя",
    props: {
      pattern: pattern,
      placeholder: "Имя (заглавными буквами)",
      maxlength: 255,
      required: true,
    },
  },
  {
    key: "patronymic",
    label: "Отчество",
    props: {
      pattern: pattern,
      placeholder: "Отчество (заглавными буквами)",
      maxlength: 255,
    },
  },
  {
    key: "birthday",
    label: "Дата рождения",
    props: { type: "date", required: true },
  },
  {
    key: "birthplace",
    label: "Место рождения",
    props: { placeholder: "Место рождения", maxlength: 255 },
  },
  {
    key: "citizenship",
    label: "Гражданство",
    props: { placeholder: "Гражданство", maxlength: 255 },
  },
  {
    key: "dual",
    label: "Двойное гражданство",
    props: { placeholder: "Двойное гражданство", maxlength: 255 },
  },
  {
    key: "snils",
    label: "СНИЛС",
    props: { pattern: "^\\d{11}$", placeholder: "СНИЛС" },
  },
  {
    key: "inn",
    label: "ИНН",
    props: { pattern: "^\\d{12}$", placeholder: "ИНН" },
  },
  {
    key: "marital",
    label: "Семейное положение",
    props: { placeholder: "Семейное положение", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительно",
    props: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
] as FormFields<Items["person"]>[];

const addresses = [
  {
    element: "select",
    key: "view",
    label: "Вид адреса",
    props: {
      items: ["Адрес регистрации", "Адрес проживания", "Другое"],
      placeholder: "Выберите адрес",
      required: true,
    },
  },
  {
    element: "textarea",
    key: "address",
    label: "Адрес",
    props: { placeholder: "Введите адрес", maxlength: 4096, required: true },
  },
] as FormFields<Items["addresses"]>[];

const affilations = [
  {
    key: "view",
    label: "Вид участия",
    props: { placeholder: "Вид участия", maxlength: 255, required: true },
  },
  {
    key: "organization",
    label: "Организация",
    props: { placeholder: "Организация", maxlength: 255, required: true },
  },
  {
    key: "inn",
    label: "ИНН",
    props: { placeholder: "Организация", pattern: "^\\d{10,12}$" },
  },
  {
    element: "textarea",
    key: "activity",
    label: "Деятельность",
    props: { placeholder: "Деятельность", maxlength: 4096 },
  },
] as FormFields<Items["affilations"]>[];

const checks = [
  {
    element: "textarea",
    key: "workplace",
    label: "Проверка по местам работы",
    props: { placeholder: "Проверка по местам работы", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "document",
    label: "Проверка документов",
    props: { placeholder: "Проверка документов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "debt",
    label: "Проверка задолженностей",
    props: { placeholder: "Проверка задолженностей", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bankruptcy",
    label: "Проверка банкротства",
    props: { placeholder: "Проверка банкротства", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "bki",
    label: "Проверка Кредитной истории",
    props: { placeholder: "Проверка Кредитной истории", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "courts",
    label: "Проверка судебных дел",
    props: { placeholder: "Проверка судебных дел", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "affilation",
    label: "Проверка аффилированности",
    props: { placeholder: "Проверка аффилированности", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "terrorist",
    label: "Проверка в списке террористов",
    props: { placeholder: "Проверка в списке террористов", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "internet",
    label: "Проверка в открытых источниках",
    props: { placeholder: "Проверка в открытых источниках", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "cronos",
    label: "Проверка в Кронос",
    props: { placeholder: "Проверка в Кронос", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "addition",
    label: "Дополнительная информация",
    props: { placeholder: "Дополнительная информация", maxlength: 4096 },
  },
  {
    element: "textarea",
    key: "comment",
    label: "Комментарий",
    props: { placeholder: "Комментарий", maxlength: 4096 },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    props: {
      items: Object.values(Conclusions),
      placeholder: "Выберите результат",
      required: true,
    },
  },
] as FormFields<Items["checks"]>[];

const contacts = [
  {
    element: "select",
    key: "view",
    label: "Вид контакта",
    props: {
      items: ["Телефон", "Электронная почта", "Другое"],
      placeholder: "Выберите контакт",
      maxlength: 255,
      required: true,
    },
  },
  {
    key: "contact",
    label: "Контакт",
    props: { placeholder: "Контакт", maxlength: 255, required: true },
  },
] as FormFields<Items["contacts"]>[];

const documents = [
  {
    element: "select",
    key: "view",
    label: "Вид документа",
    props: {
      items: ["Паспорт", "Иностранный паспорт", "Другое"],
      placeholder: "Выберите документ",
      required: true,
    },
  },
  {
    key: "series",
    label: "Серия",
    props: { placeholder: "Серия", maxlength: 16 },
  },
  {
    key: "digits",
    label: "Номер",
    props: { placeholder: "Номер", maxlength: 16, required: true },
  },
  {
    key: "agency",
    label: "Кем выдан",
    props: { placeholder: "Орган выдавший", maxlength: 255 },
  },
  {
    key: "issue",
    label: "Дата выдачи",
    props: { type: "date", required: true },
  },
] as FormFields<Items["documents"]>[];

const educations = [
  {
    element: "select",
    key: "view",
    label: "Вид образования",
    props: {
      items: [
        "Основное общее",
        "Среднее общее",
        "Среднее профессиональное",
        "Высшее",
        "Неоконченное высшее образование",
        "Другое образование",
      ],
      placeholder: "Выберите образование",
      required: true,
    },
  },
  {
    key: "institution",
    label: "Учебное заведение",
    props: {
      placeholder: "Учебное заведение",
      maxlength: 255,
      required: true,
    },
  },
  {
    key: "finished",
    label: "Год окончания",
    props: { placeholder: "Год окончания", pattern: "^\\d{4}$" },
  },
  {
    key: "specialty",
    label: "Специальность",
    props: { placeholder: "Специальность", maxlength: 255, required: true },
  },
] as FormFields<Items["educations"]>[];

const inquiries = [
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    props: { placeholder: "Информация", maxlength: 4096, required: true },
  },
  {
    key: "initiator",
    label: "Инициатор",
    props: { placeholder: "Инициатор", maxlength: 255, required: true },
  },
] as FormFields<Items["inquiries"]>[];

const investigations = [
  {
    key: "theme",
    label: "Тема проверки",
    props: { placeholder: "Тема проверки", maxlength: 255, required: true },
  },
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    props: { placeholder: "Информация", maxlength: 4096, required: true },
  },
] as FormFields<Items["investigations"]>[];

const poligrafs = [
  {
    element: "select",
    key: "theme",
    label: "Тема проверки",
    props: {
      items: [
        "Проверка кандидата",
        "Служебная проверка",
        "Служебное расследование",
        "Плановое мероприятие",
      ],
      placeholder: "Выберите тему",
      required: true,
    },
  },
  {
    element: "textarea",
    key: "results",
    label: "Результат",
    props: { placeholder: "Результат", maxlength: 4096, required: true },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    props: {
      items: Object.values(Decisions),
      placeholder: "Выберите результат",
      required: true,
    },
  },
] as FormFields<Items["poligrafs"]>[];

const previous = [
  {
    key: "surname",
    label: "Фамилия",
    props: { placeholder: "Фамилия", maxlength: 255, required: true },
  },
  {
    key: "firstname",
    label: "Имя",
    props: { placeholder: "Имя", maxlength: 255 },
  },
  {
    key: "patronymic",
    label: "Отчество",
    props: { placeholder: "Отчество", maxlength: 255 },
  },
  {
    key: "changed",
    label: "Год изменения",
    props: { placeholder: "Год изменения", pattern: "^\\d{4}$" },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина",
    props: { placeholder: "Причина изменения", maxlength: 4096 },
  },
] as FormFields<Items["previous"]>[];

const staffs = [
  {
    key: "position",
    label: "Должность",
    props: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    key: "department",
    label: "Подразделение",
    props: { placeholder: "Подразделение", maxlength: 255 },
  },
] as FormFields<Items["staffs"]>[];

const workplaces = [
  {
    key: "starts",
    label: "Начало работы",
    props: { type: "date", required: true },
  },
  {
    key: "finished",
    label: "Окончание работы",
    props: { type: "date" },
  },
  {
    key: "workplace",
    label: "Место работы",
    props: { placeholder: "Место работы", maxlength: 255, required: true },
  },
  {
    key: "position",
    label: "Должность",
    props: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    key: "address",
    label: "Адрес организации",
    props: { placeholder: "Адрес организации", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина увольнения",
    props: { placeholder: "Причина увольнения", maxlength: 4096 },
  },
] as FormFields<Items["workplaces"]>[];

export const itemsForms = {
  addresses,
  affilations,
  checks,
  contacts,
  documents,
  educations,
  inquiries,
  investigations,
  person,
  poligrafs,
  previous,
  staffs,
  workplaces,
} as { [key in keyof Items]: FormFields<Items[keyof Items]>[] };
