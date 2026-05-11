<script setup lang="ts">
import type { Inquisition, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки" },
  { key: "info", label: "Информация" },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const investigation = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.updated_at),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="investigation" />
</template>
