<script setup lang="ts">
import type { Staff } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelValue label="Должность" :value="props.item.position" />
  <ElementsLabelValue label="Департамент" :value="props.item.department" />
</template>
