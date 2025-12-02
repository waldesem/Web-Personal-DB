<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementsLabelValue label="Результаты" :value="props.item.results" />
  <ElementsLabelValue label="Заключение">
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
  </ElementsLabelValue>
  <ElementsLabelValue label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelValue>
</template>
