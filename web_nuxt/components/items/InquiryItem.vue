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
  <ElementsLabelSlot v-if="props.item.created" label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelSlot>
</template>
