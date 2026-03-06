<script setup lang="ts">
import type { StaffExt } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<StaffExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Должность" :value="props.item.position" />
  <ElementLabelValue label="Департамент" :value="props.item.department" />
</template>
