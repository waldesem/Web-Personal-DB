<script setup lang="ts">
import type { Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const document = {
  "Вид документа": props.item.view,
  "Серия документа": props.item.series,
  "Номер документа": props.item.digits,
  "Дата выдачи": props.item.issue
    ? new Date(props.item.issue).toLocaleDateString("ru-RU").split(",")[0]
    : "",
  "Кем выдан": props.item.agency,
};
</script>

<template>
  <div v-for="(value, key) in document" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
