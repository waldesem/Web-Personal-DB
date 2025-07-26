<script setup lang="ts">
import type { Needs } from '@/types';

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
    ? new Date(props.item.created).toLocaleDateString("ru-RU").split(",")[0]
    : "",
};
</script>

<template>
  <div v-for="(value, key) in inquiry" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
