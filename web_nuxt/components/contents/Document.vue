<script setup lang="ts">
import type { Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Passport,
    default: () => ({}),
  },
});

const content = {
  "Вид документа": props.item.view,
  "Серия документа": props.item.series,
  "Номер документа": props.item.digits,
  "Дата выдачи": new Date(props.item.issue)
    .toLocaleDateString("ru-RU")
    .split(",")[0],
  "Кем выдан": props.item.agency,
};
</script>

<template>
  <div v-for="(value, key) in content" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
