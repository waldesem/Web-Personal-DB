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
  <ElementLabelValue
    v-if="props.item.patronymic"
    label="Отчество"
    :value="props.item.patronymic"
  />
  <ElementLabelValue
    v-if="props.item.changed"
    label="Год изменения"
    :value="props.item.changed"
  />
  <ElementLabelValue
    v-if="props.item.reason"
    label="Причина"
    :value="props.item.reason"
  />
</template>
