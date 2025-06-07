<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    default: () => ({}),
  },
});

const inquiry = {
  Информация: props.item.info,
  Иннициатор: props.item.initiator,
  "Дата записи": props.item.created
    ? new Date(props.item.created).toLocaleString("ru-RU").split(",")[0]
    : "",
};
</script>

<template>
  <div v-for="(value, key) in inquiry" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
