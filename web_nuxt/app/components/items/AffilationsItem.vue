<script setup lang="ts">
import type { Affilation } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тип участия" :value="props.item.view" />
  <ElementLabelValue label="Организация" :value="props.item.organization" />
  <ElementLabelValue label="ИНН" :value="props.item.inn" />
</template>
