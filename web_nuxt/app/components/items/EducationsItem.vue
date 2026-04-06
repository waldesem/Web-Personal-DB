<script setup lang="ts">
import type { Education } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Уровень образования" :value="props.item.view" />
  <ElementLabelValue
    label="Учебное заведение"
    :value="props.item.institution"
  />
  <ElementLabelValue label="Год окончания" :value="props.item.finished" />
  <ElementLabelValue label="Специальность" :value="props.item.specialty" />
</template>
