<script setup lang="ts">
import type { Contact, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Вид" },
  { key: "contact", label: "Контакт" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item" />
</template>
