<script setup lang="ts">
import { refAutoReset } from "@vueuse/core";
import type { Persons } from "@/types";

const NuxtTime = resolveComponent("NuxtTime");
const UButton = resolveComponent("UButton");
const UBadge = resolveComponent("UBadge");

const props = defineProps({
  item: {
    type: Object as PropType<Persons>,
    default: () => ({}),
  },
});

const copy = refAutoReset("Копировать адрес", 3000);

const person = {
  Фамилия: props.item.surname,
  Имя: props.item.firstname,
  Отчество: props.item.patronymic,
  "Дата рождения": h(NuxtTime, {
    datetime: props.item.birthday,
  }),
  "Место рождения": props.item.birthplace,
  Гражданство: props.item.citizenship,
  "Двойное гражданство": h(UBadge, {
    variant: "outline",
    color: "error",
    label: props.item.dual,
  }),
  СНИЛС: props.item.snils,
  ИНН: props.item.inn,
  "Семейное положение": props.item.marital,
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  }),
  "Дополнительная информация": props.item.addition,
  "Материалы проверок": h(UButton, {
    variant: copy.value === "Копировать адрес" ? "outline" : "solid",
    disabled: !props.item.destination || copy.value === "Адрес скопирован!",
    color: copy.value === "Копировать адрес" ? "info" : "success",
    size: "sm",
    label: copy.value,
    onClick() {
      if (props.item.destination) {
        navigator.clipboard.writeText(props.item.destination).then(() => {
          if (copy.value) {
            copy.value = "Адрес скопирован!";
          }
        });
      }
    },
  }),
};
</script>

<template>
  <div v-for="(value, key) in person" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
