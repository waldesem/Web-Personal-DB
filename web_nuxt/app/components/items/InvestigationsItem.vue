<script setup lang="ts">
import type { InquisitionExt } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<InquisitionExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementLabelValue label="Информация" :value="props.item.info" />
  <ElementLabelValue
    label="Дата записи"
    :value="new Date(props.item.created_at).toLocaleDateString()"
  />
</template>
