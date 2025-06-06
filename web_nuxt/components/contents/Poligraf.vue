<script setup lang="ts">
import type { Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Pfo,
    default: () => ({}),
  },
});

const UBadge = resolveComponent("UBadge");

const content = {
  "Тема проверки": props.item.theme,
  Результаты: props.item.results,
  Заключение: h(UBadge, {
    color:
      props.item.conclusion === "БЕЗ ЗАМЕЧАНИЙ"
        ? "success"
        : props.item.conclusion === "С КОММЕНТАРИЯМИ"
        ? "primary"
        : "error",
    label: props.item.conclusion,
  }),
  "Дата записи": new Date(props.item.created)
    .toLocaleString("ru-RU")
    .split(",")[0],
};
</script>

<template>
  <div v-for="(value, key) in content" :key="key">
    <div v-if="value" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">{{ key }}</div>
      <div v-if="typeof value == 'object'" class="col-span-9">
        <component :is="value" />
      </div>
      <div v-else class="col-span-9 break-words">{{ value }}</div>
    </div>
  </div>
</template>
