<script setup lang="ts">
import type { Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Work,
    default: () => ({}),
  }
})
</script>

<template>
  <ElementsLabelSlot v-if="props.item.now_work" :label="'Текущая работа'">
    {{ props.item.now_work ? "Да" : "Нет" }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.item.starts" :label="'Начало работы'">
    {{ new Date(props.item.starts).toLocaleDateString("ru-RU").split(",")[0] }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.item.finished" :label="'Окончание работы'">
    {{ new Date(props.item.finished).toLocaleDateString("ru-RU").split(",")[0] }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Место работы'">
    {{ props.item.workplace }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Адрес'">
    {{ props.item.addresses }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Должность'">
    {{ props.item.position }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.item.reason" :label="'Причина увольнения'">
    {{ props.item.reason }}
  </ElementsLabelSlot>
</template>
