<script setup lang="ts">
import { localStr } from "@/utils";
import { Decisions } from "@/types";
import type { Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тема проверки" :value="props.item.theme" />
  <ElementLabelValue label="Результаты" :value="props.item.results" />
  <ElementLabelSlot label="Заключение">
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
  </ElementLabelSlot>
  <ElementLabelValue
    label="Дата записи"
    :value="localStr(props.item.created_at)"
  />
</template>
