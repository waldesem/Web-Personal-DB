<script setup lang="ts">
import type { Passport } from '@/types';

const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const document = {
  "Вид документа": props.item.view,
  "Серия документа": props.item.series,
  "Номер документа": props.item.digits,
  "Дата выдачи": h(NuxtTime, {
    datetime: props.item.issue,
  }),
  "Кем выдан": props.item.agency,
};
</script>

<template>
  <div v-for="(value, key) in document" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
