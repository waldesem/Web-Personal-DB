<script setup lang="ts">
import type { Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const workplace = {
  "Текущая работа": props.item.now_work ? "Да" : "Нет",
  "Начало работы": props.item.starts
    ? new Date(props.item.starts).toLocaleDateString("ru-RU").split(",")[0]
    : "",
  "Окончание работы": props.item.finished
    ? new Date(props.item.finished).toLocaleDateString("ru-RU").split(",")[0]
    : "",
  Место: props.item.workplace,
  Адрес: props.item.addresses,
  Должность: props.item.position,
  "Причина увольнения": props.item.reason,
};
</script>

<template>
  <div v-for="(value, key) in workplace" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
