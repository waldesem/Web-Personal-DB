<script setup lang="ts">
import { localStr } from "@/utils";
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Информация" :value="props.item.info" />
  <ElementLabelValue label="Иннициатор" :value="props.item.initiator" />
  <ElementLabelValue
    label="Дата записи"
    :value="localStr(props.item.created_at)"
  />
</template>
