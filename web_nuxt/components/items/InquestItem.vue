<script setup lang="ts">
import type { Inquisition } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementsLabelValue label="Информация" :value="props.item.info" />
  <ElementsLabelValue v-if="props.item.created" label="Дата записи">
    <template #value>
      <NuxtTime :datetime="props.item.created" />
    </template>
  </ElementsLabelValue>
</template>
