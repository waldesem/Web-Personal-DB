<script setup lang="ts">
import { localStr } from "@/utils";
import type { Inquisition } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementLabelValue label="Информация" :value="props.item.info" />
  <ElementLabelValue
    label="Дата записи"
    :value="localStr(props.item.created_at)"
  />
</template>
