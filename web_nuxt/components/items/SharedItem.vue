<script setup lang="ts">
const props = defineProps({
  view: {
    type: String,
    required: true,
  },
  item: {
    type: Object,
    default: () => ({}),
  },
});

const UBadge = resolveComponent("UBadge");

const items = {
  person: {
    Фамилия: props.item.surname,
    Имя: props.item.firstname,
    Отчество: props.item.patronymic,
    "Дата рождения": new Date(props.item.birthday).toLocaleDateString("ru-RU"),
    "Место рождения": props.item.birthplace,
    Гражданство: props.item.citizenship,
    "Двойное гражданство": props.item.dual,
    СНИЛС: props.item.snils,
    ИНН: props.item.inn,
    "Семейное положение": props.item.marital,
    "Дата записи": new Date(props.item.created).toLocaleString("ru-RU"),
    "Дополнительная информация": props.item.addition,
  },
  addresses: {
    Тип: props.item.view,
    Адрес: props.item.addresses,
  },
  affilations: {
    "Тип участия": props.item.view,
    Организация: props.item.organization,
    ИНН: props.item.inn,
  },
  contacts: {
    Вид: props.item.view,
    Контакт: props.item.contact,
  },
  documents: {
    "Вид документа": props.item.view,
    "Серия документа": props.item.series,
    "Номер документа": props.item.digits,
    "Дата выдачи": new Date(props.item.issue)
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    "Кем выдан": props.item.agency,
  },
  educations: {
    "Уровень образования": props.item.view,
    "Название учебного заведения": props.item.institution,
    "Год окончания": props.item.finished,
    Специальность: props.item.specialty,
  },
  previous: {
    Фамилия: props.item.surname,
    Имя: props.item.firstname,
    Отчество: props.item.patronymic,
    "Год изменения": props.item.changed,
    Причина: props.item.reason,
  },
  staffs: {
    Должность: props.item.position,
    Департамент: props.item.department,
  },
  workplaces: {
    "Текущая работа": props.item.now_work ? "Да" : "Нет",
    "Начало работы": new Date(props.item.starts)
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    "Окончание работы": new Date(props.item.finished)
      .toLocaleDateString("ru-RU")
      .split(",")[0],
    Место: props.item.workplace,
    Адрес: props.item.addresses,
    Должность: props.item.position,
    "Причина увольнения": props.item.reason,
  },
  inquiries: {
    Информация: props.item.info,
    Иннициатор: props.item.initiator,
    "Дата записи": new Date(props.item.created)
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  investigations: {
    "Тема проверки": props.item.theme,
    Информация: props.item.info,
    "Дата записи": new Date(props.item.created)
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  poligrafs: {
    "Тема проверки": props.item.theme,
    Результат: props.item.results,
    Заключение: h(UBadge, {
      color:
        props.item.conclusion === "БЕЗ ЗАМЕЧАНИЙ"
          ? "success"
          : props.item.conclusion === "С КОММЕНТАРИЯМИ"
          ? "primary"
          : "error",
      label: props.item.conclusion,
    }),
    "Дата записи": new Date(props.item.created)
      .toLocaleString("ru-RU")
      .split(",")[0],
  },
  checks: {
    "Проверка по местам работы": props.item.workplace,
    "Проверка документов": props.item.document,
    "Проверка задолженностей": props.item.debt,
    "Проверка банкротства": props.item.bankruptcy,
    "Проверка по БКИ": props.item.bki,
    "Проверка судебных решений": props.item.courts,
    "Проверка аффилированности": props.item.affilation,
    "Проверка по списку террористов": props.item.terrorist,
    "Проверка в открытых источниках": props.item.internet,
    "Проверка Кронос": props.item.cronos,
    "Дополнительная информация": props.item.addition,
    Комментарии: props.item.comment,
    Результат: h(UBadge, {
      color:
        props.item.conclusion === "СОГЛАСОВАНО"
          ? "success"
          : props.item.conclusion === "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
          ? "primary"
          : props.item.conclusion === "СНЯТ С ПРОВЕРКИ"
          ? "warning"
          : "error",

      label: props.item.conclusion,
    }),
    "Дата записи": new Date(props.item.created).toLocaleString("ru-RU"),
  },
};
</script>

<template>
  <div
    v-for="(value, key) in items[props.view as keyof typeof items]"
    :key="key"
  >
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-3">
      <div class="col-span-3">{{ key }}</div>
      <div v-if="typeof value == 'object'" class="col-span-9">
        <component :is="value" />
      </div>
      <div v-else class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
