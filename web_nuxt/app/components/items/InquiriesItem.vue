<script setup lang="ts">
import type { ItemField, Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
});

const fields = [
  { key: "info", label: "Информация" },
  { key: "initiator", label: "Инициатор" },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const inquiry = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.updated_at),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="inquiry" />
</template>
