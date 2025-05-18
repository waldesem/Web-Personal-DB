<script setup lang="ts">
import type { Address } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Address,
    default: () => ({}),
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Тип'">{{ props.item.view }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Адрес'">{{ props.item.addresses }}</ElementsLabelSlot>
</template>
