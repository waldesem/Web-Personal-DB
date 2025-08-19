<script setup lang="ts">
import type { Education } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelValue label="Уровень образования" :value="props.item.view" />
  <ElementsLabelValue
    label="Учебное заведение"
    :value="props.item.institution"
  />
  <ElementsLabelValue label="Год окончания" :value="props.item.finished" />
  <ElementsLabelValue label="Специальность" :value="props.item.specialty" />
</template>
