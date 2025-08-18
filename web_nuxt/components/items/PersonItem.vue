<script setup lang="ts">
import type { Persons } from "@/types";

const NuxtTime = resolveComponent("NuxtTime");
const UButton = resolveComponent("UButton");

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
  "Материалы проверок": h(
    UButton,
    {
      variant: "outline",
      size: "sm",
      onClick() {
        navigator.clipboard
          .writeText(
            props.item.destination
              ? props.item.destination
              : "Отсутствует путь к папке"
          )
          .then(() => {
            alert("Путь скопирован!");
          });
      },
    },
    { default: () => "Копировать адрес" }
  ),
};
</script>

<template>
  <div v-for="(value, key) in person" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
