<script setup lang="ts">
import type { Staff } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Staff,
    default: () => ({}),
  }
})
</script>

<template>
  <ElementsLabelSlot :label="'Должность'">
    {{ props.item.position }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Департамент'">
    {{ props.item.department }}
  </ElementsLabelSlot>
</template>
