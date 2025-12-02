<script setup lang="ts">
import type { Previous } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    required: true,
  },
});
</script>

<template>
  <ElementsLabelValue label="Фамилия" :value="props.item.surname" />
  <ElementsLabelValue label="Имя" :value="props.item.firstname" />
  <ElementsLabelValue label="Отчество" :value="props.item.patronymic" />
  <ElementsLabelValue label="Год изменения" :value="props.item.changed" />
  <ElementsLabelValue label="Причина" :value="props.item.reason" />
</template>
