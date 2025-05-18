<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Needs,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelSlot :label="'Информация'">{{
    props.item.info
  }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Иннициатор'">{{
    props.item.initiator
  }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.item.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
</template>