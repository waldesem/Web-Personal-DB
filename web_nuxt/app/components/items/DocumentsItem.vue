<script setup lang="ts">
import { localStr } from "@/utils";
import type { Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Вид документа" :value="props.item.view" />
  <ElementLabelValue label="Серия документа" :value="props.item.series" />
  <ElementLabelValue label="Номер документа" :value="props.item.digits" />
  <ElementLabelValue label="Кем выдан" :value="props.item.agency" />
  <ElementLabelValue label="Дата выдачи" :value="localStr(props.item.issue)" />
</template>
