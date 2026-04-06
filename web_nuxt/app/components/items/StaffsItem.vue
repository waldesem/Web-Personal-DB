<script setup lang="ts">
import type { Staff } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Должность" :value="props.item.position" />
  <ElementLabelValue label="Департамент" :value="props.item.department" />
</template>
