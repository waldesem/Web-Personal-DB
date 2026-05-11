<script setup lang="ts">
import type { Affilation, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Тип участия" },
  { key: "organization", label: "Организация" },
  { key: "inn", label: "ИНН" },
  { key: "activity", label: "Деятельность" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item" />
</template>
