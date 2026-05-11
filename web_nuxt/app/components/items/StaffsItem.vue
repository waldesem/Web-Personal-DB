<script setup lang="ts">
import type { ItemField, Staff } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    required: true,
  },
});

const fields = [
  { key: "position", label: "Должность" },
  { key: "department", label: "Департамент" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item" />
</template>
