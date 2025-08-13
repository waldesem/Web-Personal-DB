<script setup lang="ts">
import type { Needs } from '@/types';

const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    default: () => ({}),
  },
});

const inquiry = {
  Информация: props.item.info,
  Иннициатор: props.item.initiator,
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  })
};
</script>

<template>
  <div v-for="(value, key) in inquiry" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
