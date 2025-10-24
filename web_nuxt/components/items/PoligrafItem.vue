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
  <ElementsLabelValue v-if="props.item.conclusion" label="Заключение">
    <template #value>
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
    </template>
  </ElementsLabelValue>
  <ElementsLabelValue v-if="props.item.created" label="Дата записи">
    <template #value>
      <NuxtTime :datetime="props.item.created" />
    </template>
  </ElementsLabelValue>
</template>
