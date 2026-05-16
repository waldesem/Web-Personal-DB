import { localStr } from "@/utils";
import type { ItemField, Items } from "@/types";

export const divsFields = {
  addresses: [
    { key: "view", label: "Вид адреса" },
    { key: "address", label: "Адрес" },
  ],
  affilations: [
    { key: "view", label: "Вид участия" },
    { key: "organization", label: "Организация" },
    { key: "inn", label: "ИНН" },
    { key: "activity", label: "Деятельность" },
  ],
  checks: [
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
    { key: "conclusion", label: "Результат" },
    { key: "created", label: "Дата записи", div: (div) => localStr(div) },
  ],
  contacts: [
    { key: "view", label: "Вид контакта" },
    { key: "contact", label: "Контакт" },
  ],
  documents: [
    { key: "view", label: "Вид документа" },
    { key: "series", label: "Серия документа" },
    { key: "digits", label: "Номер документа" },
    { key: "agency", label: "Кем выдан" },
    { key: "issue", label: "Дата выдачи", div: (div) => localStr(div) },
  ],
  educations: [
    { key: "view", label: "Вид образования" },
    { key: "institution", label: "Учебное заведение" },
    { key: "finished", label: "Год окончания" },
    { key: "specialty", label: "Специальность" },
  ],
  inquiries: [
    { key: "info", label: "Информация" },
    { key: "initiator", label: "Инициатор" },
    { key: "created", label: "Дата записи", div: (div) => localStr(div) },
  ],
  investigations: [
    { key: "theme", label: "Тема проверки" },
    { key: "info", label: "Информация" },
    { key: "created", label: "Дата записи", div: (div) => localStr(div) },
  ],
  poligrafs: [
    { key: "theme", label: "Тема проверки" },
    { key: "results", label: "Результат" },
    { key: "conclusion", label: "Результат" },
    { key: "created", label: "Дата записи", div: (div) => localStr(div) },
  ],
  previous: [
    { key: "surname", label: "Фамилия" },
    { key: "firstname", label: "Имя" },
    { key: "patronymic", label: "Отчество" },
    { key: "changed", label: "Год изменения" },
    { key: "reason", label: "Причина" },
  ],
  staffs: [
    { key: "position", label: "Должность" },
    { key: "department", label: "Подразделение" },
  ],
  workplaces: [
    { key: "nowWork", label: "Текущая работа" },
    { key: "starts", label: "Начало работы", div: (div) => localStr(div) },
    { key: "finished", label: "Окончание работы", div: (div) => localStr(div) },
    { key: "workplace", label: "Место работы" },
    { key: "position", label: "Должность" },
    { key: "address", label: "Адрес организации" },
    { key: "reason", label: "Причина увольнения" },
  ],
} as { [key in keyof Items]: ItemField[] };
