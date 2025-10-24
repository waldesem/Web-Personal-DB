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
  <ElementsLabelValue label="Вид документа" :value="props.item.view" />
  <ElementsLabelValue label="Серия документа" :value="props.item.series" />
  <ElementsLabelValue label="Номер документа" :value="props.item.digits" />
  <ElementsLabelValue label="Кем выдан" :value="props.item.agency" />
  <ElementsLabelValue v-if="props.item.issue" label="Дата выдачи">
    <template #value>
      <NuxtTime :datetime="props.item.issue" />
    </template>
  </ElementsLabelValue>
</template>
