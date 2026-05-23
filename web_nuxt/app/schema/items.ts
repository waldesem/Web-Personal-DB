import { h } from "vue";
import { localStr } from "@/utils";
import { Conclusions, Decisions } from "@/types";
import type { Items, ItemFields } from "@/types";

export const person = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  {
    key: "birthday",
    label: "Дата рождения",
    div: (row) => localStr(row.birthday),
  },
  { key: "birthplace", label: "Место рождения" },
  { key: "citizenship", label: "Гражданство" },
  { key: "dual", label: "Двойное гражданство" },
  { key: "snils", label: "СНИЛС" },
  { key: "inn", label: "ИНН" },
  { key: "marital", label: "Семейное положение" },
  { key: "addition", label: "Дополнительная информация" },
  {
    key: "created",
    label: "Дата записи",
    div: (row) => localStr(row.updated_at),
  },
  { key: "destination", label: "Материалы проверок", slot: true },
] as ItemFields<Items["person"]>[];

const addresses = [
  { key: "view", label: "Вид адреса" },
  { key: "address", label: "Адрес" },
] as ItemFields<Items["addresses"]>[];

const affilations = [
  { key: "view", label: "Вид участия" },
  { key: "organization", label: "Организация" },
  { key: "inn", label: "ИНН" },
  { key: "activity", label: "Деятельность" },
] as ItemFields<Items["affilations"]>[];

const checks = [
  { key: "workplace", label: "Проверка по местам работы" },
  { key: "document", label: "Проверка документов" },
  { key: "debt", label: "Проверка задолженностей" },
  { key: "bankruptcy", label: "Проверка банкротства" },
  { key: "bki", label: "Проверка Кредитной истории" },
  { key: "courts", label: "Проверка судебных дел" },
  { key: "affilation", label: "Проверка аффилированности" },
  { key: "terrorist", label: "Проверка в списке террористов" },
  { key: "internet", label: "Проверка в открытых источниках" },
  { key: "cronos", label: "Проверка в Кронос" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "comment", label: "Комментарий" },
  {
    key: "conclusion",
    label: "Результат",
    component: (row) => {
      const color =
        row.conclusion === Conclusions.agreed
          ? "bg-green-500"
          : row.conclusion === Conclusions.cancel
            ? "bg-gray-500"
            : row.conclusion === Conclusions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return h(
        "span",
        {
          class: [
            "flex inline-flex items-center py-1 px-2 rounded-md text-sm text-white",
            color,
          ],
        },
        row.conclusion,
      );
    },
  },
  {
    key: "created",
    label: "Дата записи",
    div: (row) => localStr(row.updated_at),
  },
] as ItemFields<Items["checks"]>[];

const contacts = [
  { key: "view", label: "Вид контакта" },
  { key: "contact", label: "Контакт" },
] as ItemFields<Items["contacts"]>[];

const documents = [
  { key: "view", label: "Вид документа" },
  { key: "series", label: "Серия документа" },
  { key: "digits", label: "Номер документа" },
  { key: "agency", label: "Кем выдан" },
  { key: "issue", label: "Дата выдачи", div: (row) => localStr(row.issue) },
] as ItemFields<Items["documents"]>[];

const educations = [
  { key: "view", label: "Вид образования" },
  { key: "institution", label: "Учебное заведение" },
  { key: "finished", label: "Год окончания" },
  { key: "specialty", label: "Специальность" },
] as ItemFields<Items["educations"]>[];

const inquiries = [
  { key: "info", label: "Информация" },
  { key: "initiator", label: "Инициатор" },
  {
    key: "created",
    label: "Дата записи",
    div: (row) => localStr(row.updated_at),
  },
] as ItemFields<Items["inquiries"]>[];

const investigations = [
  { key: "theme", label: "Тема проверки" },
  { key: "info", label: "Информация" },
  {
    key: "created",
    label: "Дата записи",
    div: (row) => localStr(row.updated_at),
  },
] as ItemFields<Items["investigations"]>[];

const poligrafs = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результат" },
  {
    key: "conclusion",
    label: "Результат",
    component: (row) => {
      const color =
        row.conclusion === Decisions.agreed
          ? "bg-green-500"
          : row.conclusion === Decisions.cancel
            ? "bg-gray-500"
            : row.conclusion === Decisions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return h(
        "span",
        {
          class: [
            "flex inline-flex items-center py-1 px-2 rounded-md text-sm text-white",
            color,
          ],
        },
        row.conclusion,
      );
    },
  },
  {
    key: "created",
    label: "Дата записи",
    div: (row) => localStr(row.updated_at),
  },
] as ItemFields<Items["poligrafs"]>[];

const previous = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "changed", label: "Год изменения" },
  { key: "reason", label: "Причина" },
] as ItemFields<Items["previous"]>[];

const staffs = [
  { key: "position", label: "Должность" },
  { key: "department", label: "Подразделение" },
] as ItemFields<Items["staffs"]>[];

const workplaces = [
  { key: "starts", label: "Начало работы", div: (row) => localStr(row.starts) },
  {
    key: "finished",
    label: "Окончание работы",
    div: (row) => localStr(row.finished),
  },
  { key: "workplace", label: "Место работы" },
  { key: "position", label: "Должность" },
  { key: "address", label: "Адрес организации" },
  { key: "reason", label: "Причина увольнения" },
] as ItemFields<Items["workplaces"]>[];

export const itemsFields = {
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
} as { [key in keyof Items]: ItemFields<Items[keyof Items]>[] };
