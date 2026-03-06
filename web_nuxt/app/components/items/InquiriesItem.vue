<script setup lang="ts">
import type { NeedsExt } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<NeedsExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Информация" :value="props.item.info" />
  <ElementLabelValue label="Иннициатор" :value="props.item.initiator" />
  <ElementLabelValue
    label="Дата записи"
    :value="new Date(props.item.created_at).toLocaleDateString()"
  />
</template>
