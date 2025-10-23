<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementsLabelValue label="Результаты" :value="props.item.results" />
  <ElementsLabelSlot v-if="props.item.conclusion" label="Заключение">
    <UBadge
      :color="
        props.item.conclusion === Decisions.agreed
          ? 'success'
          : props.item.conclusion === Decisions.comments
          ? 'warning'
          : props.item.conclusion === Decisions.cancel
          ? 'neutral'
          : 'error'
      "
      :label="props.item.conclusion"
    />
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.item.created" label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelSlot>
</template>
