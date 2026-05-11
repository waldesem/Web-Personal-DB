<script setup lang="ts">
import type { ItemField, Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Вид документа" },
  { key: "series", label: "Серия документа" },
  { key: "digits", label: "Номер документа" },
  { key: "agency", label: "Кем выдан" },
  { key: "issue", label: "Дата выдачи" },
] as ItemField[];

const doc = computed(() => {
  return {
    ...props.item,
    issue: localStr(props.item.issue),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="doc" />
</template>
