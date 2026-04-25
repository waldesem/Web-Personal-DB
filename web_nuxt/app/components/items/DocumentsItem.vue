<script setup lang="ts">
import type { Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Вид документа" :value="props.item.view" />
  <ElementLabelValue
    v-if="props.item.series"
    label="Серия документа"
    :value="props.item.series"
  />
  <ElementLabelValue label="Номер документа" :value="props.item.digits" />
  <ElementLabelValue
    v-if="props.item.agency"
    label="Кем выдан"
    :value="props.item.agency"
  />
  <ElementLabelValue
    label="Дата выдачи"
    :value="new Date(props.item.issue).toLocaleDateString()"
  />
</template>
