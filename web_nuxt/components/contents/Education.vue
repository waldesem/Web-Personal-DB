<script setup lang="ts">
import type { Education } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Education,
    default: () => ({}),
  },
});

const content = {
  "Уровень образования": props.item.view,
  "Название учебного заведения": props.item.institution,
  "Год окончания": props.item.finished,
  Специальность: props.item.specialty,
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
