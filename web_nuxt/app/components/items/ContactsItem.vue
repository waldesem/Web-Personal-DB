<script setup lang="ts">
import type { ContactExt } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<ContactExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Вид" :value="props.item.view" />
  <ElementLabelValue label="Контакт" :value="props.item.contact" />
</template>
