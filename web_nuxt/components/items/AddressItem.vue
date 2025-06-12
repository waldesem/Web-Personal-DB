<script setup lang="ts">
import type { Address } from '@/types';

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
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
