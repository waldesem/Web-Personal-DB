<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
});
</script>

<template>
  <ElementsLabelValue label="Информация" :value="props.item.info" />
  <ElementsLabelValue label="Иннициатор" :value="props.item.initiator" />
  <ElementsLabelValue label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelValue>
</template>
