<script setup lang="ts">
import type { ItemField, Previous } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    required: true,
  },
});

const fields = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "changed", label: "Год изменения" },
  { key: "reason", label: "Причина" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item" />
</template>
