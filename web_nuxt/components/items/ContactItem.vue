<script setup lang="ts">
import type { Contact } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Вид'">{{ props.item.view }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Контакт'">{{ props.item.contact }}</ElementsLabelSlot>
</template>
