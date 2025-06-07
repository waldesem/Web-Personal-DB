<script setup lang="ts">
import type { Address } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const address = {
  Тип: props.item.view,
  Адрес: props.item.addresses,
};
</script>

<template>
  <div v-for="(value, key) in address" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
