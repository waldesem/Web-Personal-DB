<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
});
</script>

<template>
  <ElementsLabelSlot :label="'ID запроса'">
    {{ props.item.id }}
  </ElementsLabelSlot>
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