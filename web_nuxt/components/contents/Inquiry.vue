<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Needs,
    default: () => ({}),
  },
});

const content = {
  Информация: props.item.info,
  Иннициатор: props.item.initiator,
  "Дата записи": new Date(props.item.created)
    .toLocaleString("ru-RU")
    .split(",")[0],
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
