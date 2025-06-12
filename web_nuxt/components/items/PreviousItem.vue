<script setup lang="ts">
import type { Previous } from '@/types';

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    default: () => ({}),
  },
});

const previous = {
  Фамилия: props.item.surname,
  Имя: props.item.firstname,
  Отчество: props.item.patronymic,
  "Год изменения": props.item.changed,
  Причина: props.item.reason,
};
</script>

<template>
  <div v-for="(value, key) in previous" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
