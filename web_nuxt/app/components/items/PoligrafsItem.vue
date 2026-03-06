<script setup lang="ts">
import type { PfoExt } from "@/types";
import { Decisions } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<PfoExt>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementLabelValue label="Результаты" :value="props.item.results" />
  <ElementLabelValue label="Заключение">
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
  </ElementLabelValue>
  <ElementLabelValue
    label="Дата записи"
    :value="new Date(props.item.created_at).toLocaleDateString()"
  />
</template>
