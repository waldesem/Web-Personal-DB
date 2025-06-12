<script setup lang="ts">
import type { Education } from '@/types';

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    default: () => ({}),
  },
});

const education = {
  "Уровень образования": props.item.view,
  "Название учебного заведения": props.item.institution,
  "Год окончания": props.item.finished,
  Специальность: props.item.specialty,
};
</script>

<template>
  <div v-for="(value, key) in education" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
