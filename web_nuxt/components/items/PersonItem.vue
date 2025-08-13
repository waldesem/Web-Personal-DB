<script setup lang="ts">
import type { Persons } from "@/types";

const NuxtTime = resolveComponent("NuxtTime");

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
  "Дата рождения": h(NuxtTime, {
    datetime: props.item.birthday,
  }),
  "Место рождения": props.item.birthplace,
  Гражданство: props.item.citizenship,
  "Двойное гражданство": props.item.dual,
  СНИЛС: props.item.snils,
  ИНН: props.item.inn,
  "Семейное положение": props.item.marital,
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  }),
  "Дополнительная информация": props.item.addition,
  "Материалы проверок": props.item.destination,
};
</script>

<template>
  <div v-for="(value, key) in person" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
