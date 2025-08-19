<script setup lang="ts">
import type { Inquisition } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementsLabelValue label="Информация" :value="props.item.info" />
  <ElementsLabelSlot v-if="props.item.created" label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelSlot>
</template>
