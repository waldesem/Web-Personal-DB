<script setup lang="ts">
import type { Affilation } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    default: () => ({}),
  },
});

const affilation = {
  "Тип участия": props.item.view,
    Организация: props.item.organization,
    ИНН: props.item.inn,
};
</script>

<template>
  <div v-for="(value, key) in affilation" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
