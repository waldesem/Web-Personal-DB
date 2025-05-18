<script setup lang="ts">
import type { Inquisition } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Inquisition,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelSlot :label="'Тема проверки'">{{
    props.item.theme
  }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Информация'">{{
    props.item.info
  }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.item.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
</template>
