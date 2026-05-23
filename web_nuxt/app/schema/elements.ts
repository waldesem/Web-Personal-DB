import { localStr, timeAgoStr } from "@/utils";
import type { TableColumn } from "@nuxt/ui";
import type { Candidate, Items } from "@/types";
// import type { icons } from "@iconify-json/lucide/index.js";

// Определяем массив данных для таблицы кандидатов
export const personColumns: TableColumn<Candidate>[] = [
  { accessorKey: "id", header: "#" },
  {
    accessorKey: "surname",
    header: "Фамилия",
  },
  {
    accessorKey: "firstname",
    header: "Имя",
  },
  {
    accessorKey: "patronymic",
    header: "Отчество",
    cell: ({ row }) => {
      return row.getValue("patronymic") ?? "";
    },
  },
  {
    accessorKey: "birthday",
    header: "Дата рождения",
    cell: ({ row }) => {
      return localStr(row.getValue("birthday"));
    },
  },
  {
    accessorKey: "updated_at",
    header: "Обновлено",
    cell: ({ row }) => {
      return timeAgoStr(row.getValue("updated_at"));
    },
  },
  {
    accessorKey: "username",
    header: "Сотрудник",
    cell: ({ row }) => {
      return row.original.username.split(" ")[0];
    },
  },
];

export const anketaTab = { label: "Анкета", slot: "person" as keyof Items };

export const itemsTabs = [
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
] as { label: string; icon: string; slot: keyof Items }[];

export const itemsAccordion = [
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
] as { label: string; icon: string; slot: keyof Items }[];
