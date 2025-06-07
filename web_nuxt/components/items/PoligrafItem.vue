<script setup lang="ts">
import type { Pfo } from "@/types";

const UBadge = resolveComponent("UBadge");

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
      props.item.conclusion === "БЕЗ ЗАМЕЧАНИЙ"
        ? "success"
        : props.item.conclusion === "С КОММЕНТАРИЯМИ"
        ? "primary"
        : props.item.conclusion === "ОТКАЗ ОТ ПРОВЕРКИ"
        ? "warning"
        : "error",
    label: props.item.conclusion,
  }),
  "Дата записи": props.item.created
    ? new Date(props.item.created).toLocaleString("ru-RU").split(",")[0]
    : "",
};
</script>

<template>
  <div v-for="(value, key) in poligraf" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
