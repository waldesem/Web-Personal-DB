<script setup lang="ts">
import type { Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Passport,
    default: {} as Passport,
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Вид документа'">{{ props.item.view }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Серия документа'">{{ props.item.series }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Номер документа'">{{ props.item.digits }}</ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.item.issue" :label="'Дата выдачи'">
    {{ new Date(props.item.issue).toLocaleDateString("ru-RU").split(",")[0] }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Кем выдан'">{{ props.item.agency }}</ElementsLabelSlot>
</template>
