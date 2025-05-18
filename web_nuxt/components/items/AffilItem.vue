<script setup lang="ts">
import type { Affilation } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Affilation,
    default: () => ({}),
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Тип участия'">{{ props.item.view }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Организация'">{{ props.item.organization }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'ИНН'">{{ props.item.inn }}</ElementsLabelSlot>
</template>
