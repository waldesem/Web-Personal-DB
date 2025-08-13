<script setup lang="ts">
import type { Work } from "@/types";

const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const workplace = {
  "Текущая работа": props.item.now_work ? "Да" : "Нет",
  "Начало работы": props.item.starts ? h(NuxtTime, {
    datetime: props.item.starts,
  }) : "",
  "Окончание работы": props.item.finished ? h(NuxtTime, {
    datetime: props.item.finished,
  }) : "",
  Место: props.item.workplace,
  Адрес: props.item.address,
  Должность: props.item.position,
  "Причина увольнения": props.item.reason,
};
</script>

<template>
  <div v-for="(value, key) in workplace" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
