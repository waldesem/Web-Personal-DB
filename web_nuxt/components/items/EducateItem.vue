<script setup lang="ts">
import type { Education } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Education,
    default: () => ({}),
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Уровень образования'">{{ props.item.view }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Название учебного заведения'">{{ props.item.institution }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Год окончания'">{{ props.item.finished }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Специальность'">{{ props.item.specialty }}</ElementsLabelSlot>
</template>
