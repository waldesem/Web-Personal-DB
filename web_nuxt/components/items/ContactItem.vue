<script setup lang="ts">
import type { Contact } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const contact = {
  Вид: props.item.view,
  Контакт: props.item.contact,
};
</script>

<template>
  <div v-for="(value, key) in contact" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
