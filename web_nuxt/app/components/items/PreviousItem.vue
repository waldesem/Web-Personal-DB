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
  <ElementLabelValue label="Фамилия" :value="props.item.surname" />
  <ElementLabelValue label="Имя" :value="props.item.firstname" />
  <ElementLabelValue label="Отчество" :value="props.item.patronymic" />
  <ElementLabelValue label="Год изменения" :value="props.item.changed" />
  <ElementLabelValue label="Причина" :value="props.item.reason" />
</template>
