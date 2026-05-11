<script setup lang="ts">
import type { Education, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Уровень образования" },
  { key: "institution", label: "Учебное заведение" },
  { key: "finished", label: "Год окончания" },
  { key: "specialty", label: "Специальность" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item" />
</template>
