<script setup lang="ts">
import type { PassportExt } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<PassportExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Вид документа" :value="props.item.view" />
  <ElementLabelValue label="Серия документа" :value="props.item.series" />
  <ElementLabelValue label="Номер документа" :value="props.item.digits" />
  <ElementLabelValue label="Кем выдан" :value="props.item.agency" />
  <ElementLabelValue
    label="Дата выдачи"
    :value="new Date(props.item.issue).toLocaleDateString()"
  />
</template>
