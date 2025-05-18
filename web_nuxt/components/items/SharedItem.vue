<script setup lang="ts">
import type { DivsType, TabsType, Persons } from "@/types";

const props = defineProps({
  view: {
    type: String,
    required: true,
  },
  item: {
    type: Object as () => DivsType | TabsType | Persons,
    default: () => ({}),
  },
});

const UBadge = resolveComponent("UBadge");

const items = {
  person: {
    Фамилия: props.item["surname" as keyof typeof props.item],
    Имя: props.item["firstname" as keyof typeof props.item],
    Отчество: props.item["patronymic" as keyof typeof props.item],
    "Дата рождения": new Date(
      props.item["birthday" as keyof typeof props.item]
    ).toLocaleDateString("ru-RU"),
    "Место рождения": props.item["birthplace" as keyof typeof props.item],
    Гражданство: props.item["citizenship" as keyof typeof props.item],
    "Двойное гражданство": props.item["dual" as keyof typeof props.item],
    СНИЛС: props.item["snils" as keyof typeof props.item],
    ИНН: props.item["inn" as keyof typeof props.item],
    "Семейное положение": props.item["marital" as keyof typeof props.item],
    "Дата записи": props.item["created" as keyof typeof props.item],
    "Дополнительная информация":
      props.item["addition" as keyof typeof props.item],
  },
  addresses: {
    Тип: props.item["view" as keyof typeof props.item],
    Адрес: props.item["addresses" as keyof typeof props.item],
  },
  affilations: {
    "Тип участия": props.item["view" as keyof typeof props.item],
    Организация: props.item["organization" as keyof typeof props.item],
    ИНН: props.item["inn" as keyof typeof props.item],
  },
  contacts: {
    Вид: props.item["view" as keyof typeof props.item],
    Контакт: props.item["contact" as keyof typeof props.item],
  },
  documents: {
    "Вид документа": props.item["view" as keyof typeof props.item],
    "Серия документа": props.item["series" as keyof typeof props.item],
    "Номер документа": props.item["digits" as keyof typeof props.item],
    "Дата выдачи": new Date(props.item["issue" as keyof typeof props.item])
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    "Кем выдан": props.item["agency" as keyof typeof props.item],
  },
  educations: {
    "Уровень образования": props.item["view" as keyof typeof props.item],
    "Название учебного заведения":
      props.item["institution" as keyof typeof props.item],
    "Год окончания": props.item["finished" as keyof typeof props.item],
    Специальность: props.item["specialty" as keyof typeof props.item],
  },
  previous: {
    Фамилия: props.item["surname" as keyof typeof props.item],
    Имя: props.item["firstname" as keyof typeof props.item],
    Отчество: props.item["patronymic" as keyof typeof props.item],
    "Год изменения": props.item["changed" as keyof typeof props.item],
    Причина: props.item["reason" as keyof typeof props.item],
  },
  workplaces: {
    Должность: props.item["position" as keyof typeof props.item],
    Департамент: props.item["department" as keyof typeof props.item],
  },
  work: {
    "Текущая работа": props.item["now_work" as keyof typeof props.item]
      ? "Да"
      : "Нет",
    "Начало работы": new Date(props.item["starts" as keyof typeof props.item])
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    "Окончание работы": new Date(
      props.item["finished" as keyof typeof props.item]
    )
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    Место: props.item["workplace" as keyof typeof props.item],
    Адрес: props.item["addresses" as keyof typeof props.item],
    Должность: props.item["position" as keyof typeof props.item],
    "Причина увольнения": props.item["reason" as keyof typeof props.item],
  },
  inquiries: {
    Информация: props.item["info" as keyof typeof props.item],
    Иннициатор: props.item["initiator" as keyof typeof props.item],
    "Дата записи": new Date(props.item["created" as keyof typeof props.item])
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  investigations: {
    "Тема проверки": props.item["theme" as keyof typeof props.item],
    Информация: props.item["info" as keyof typeof props.item],
    "Дата записи": new Date(props.item["created" as keyof typeof props.item])
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  poligrafs: {
    "Тема проверки": props.item["theme" as keyof typeof props.item],
    Результат: props.item["results" as keyof typeof props.item],
    Заключение: h(UBadge, {
      color:
        props.item["conclusion" as keyof typeof props.item] === "БЕЗ ЗАМЕЧАНИЙ"
          ? "success"
          : props.item["conclusion" as keyof typeof props.item] ===
            "С КОММЕНТАРИЯМИ"
          ? "primary"
          : "error",

      label: props.item["conclusion" as keyof typeof props.item],
      variant: "soft",
    }),
    "Дата записи": new Date(props.item["created" as keyof typeof props.item])
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  checks: {
    "Проверка по местам работы":
      props.item["workplace" as keyof typeof props.item],
    "Проверка документов": props.item["document" as keyof typeof props.item],
    "Проверка задолженностей": props.item["debt" as keyof typeof props.item],
    "Проверка банкротства": props.item["bankruptcy" as keyof typeof props.item],
    "Проверка по БКИ": props.item["bki" as keyof typeof props.item],
    "Проверка судебных решений":
      props.item["courts" as keyof typeof props.item],
    "Проверка аффилированности":
      props.item["affilation" as keyof typeof props.item],
    "Проверка по списку террористов":
      props.item["terrorist" as keyof typeof props.item],
    "Проверка в открытых источниках":
      props.item["internet" as keyof typeof props.item],
    "Проверка Кронос": props.item["cronos" as keyof typeof props.item],
    "Дополнительная информация":
      props.item["addition" as keyof typeof props.item],
    Комментарии: props.item["comment" as keyof typeof props.item],
    Результат: h(UBadge, {
      color:
        props.item["conclusion" as keyof typeof props.item] === "СОГЛАСОВАНО"
          ? "success"
          : props.item["conclusion" as keyof typeof props.item] ===
            "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
          ? "primary"
          : props.item["conclusion" as keyof typeof props.item] ===
            "СНЯТ С ПРОВЕРКИ"
          ? "warning"
          : "error",

      label: props.item["conclusion" as keyof typeof props.item],
      variant: "soft",
    }),
    "Дата записи": new Date(
      props.item["created" as keyof typeof props.item]
    ).toLocaleString("ru-RU"),
  },
};
</script>

<template>
  <div
    v-for="(value, key) in items[props.view as keyof typeof items]"
    :key="key"
  >
    <div class="flex grid grid-cols-12 gap-3 mb-3">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
