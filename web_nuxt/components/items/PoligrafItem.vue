<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "@/types";

const UBadge = resolveComponent("UBadge");
const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const poligraf = {
  "Тема проверки": props.item.theme,
  Результаты: props.item.results,
  Заключение: h(UBadge, {
    color:
      props.item.conclusion === Decisions.agreed
        ? "success"
        : props.item.conclusion === Decisions.comments
        ? "warning"
        : props.item.conclusion === Decisions.cancel
        ? "neutral"
        : "error",
    label: props.item.conclusion,
  }),
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  })
};
</script>

<template>
  <div v-for="(value, key) in poligraf" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
