<script setup lang="ts">
import type { Inquisition } from '@/types';

const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const investigation = {
  "Тема проверки": props.item.theme,
  Информация: props.item.info,
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  })
};
</script>

<template>
  <div v-for="(value, key) in investigation" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
