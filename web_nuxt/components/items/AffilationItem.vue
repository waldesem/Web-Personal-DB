<script setup lang="ts">
import type { Affilation } from '@/types';

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    required: true,
  },
});
</script>

<template>
  <ElementsLabelValue label="Тип участия" :value="props.item.view" />
  <ElementsLabelValue label="Организация" :value="props.item.organization" />
  <ElementsLabelValue label="ИНН" :value="props.item.inn" />
</template>
