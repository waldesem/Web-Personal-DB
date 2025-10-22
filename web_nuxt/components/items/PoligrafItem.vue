<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "@/types";

const props = defineProps<Pfo>()
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.theme" />
  <ElementsLabelValue label="Результаты" :value="props.results" />
  <ElementsLabelSlot v-if="props.conclusion" label="Заключение">
    <UBadge
      :color="
        props.conclusion === Decisions.agreed
          ? 'success'
          : props.conclusion === Decisions.comments
          ? 'warning'
          : props.conclusion === Decisions.cancel
          ? 'neutral'
          : 'error'
      "
      :label="props.conclusion"
    />
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.created" label="Дата записи">
    <NuxtTime :datetime="props.created" />
  </ElementsLabelSlot>
</template>
