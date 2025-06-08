<script setup lang="ts">
import type { Persons } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Persons>,
    default: () => ({}),
  },
});

const person = {
  Фамилия: props.item.surname,
  Имя: props.item.firstname,
  Отчество: props.item.patronymic,
  "Дата рождения": props.item.birthday
    ? new Date(props.item.birthday).toLocaleDateString("ru-RU")
    : "",
  "Место рождения": props.item.birthplace,
  Гражданство: props.item.citizenship,
  "Двойное гражданство": props.item.dual,
  СНИЛС: props.item.snils,
  ИНН: props.item.inn,
  "Семейное положение": props.item.marital,
  "Дата записи": props.item.created
    ? new Date(props.item.created).toLocaleString("ru-RU")
    : "",
  "Дополнительная информация": props.item.addition,
  "Материалы проверок": props.item.destination,
};
</script>

<template>
  <div v-for="(value, key) in person" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
