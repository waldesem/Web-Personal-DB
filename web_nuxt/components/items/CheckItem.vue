<script setup lang="ts">
import type { Verification } from "@/types";
import { Conclusions } from "@/types";

const UBadge = resolveComponent("UBadge");
const NuxtTime = resolveComponent("NuxtTime");

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    default: () => ({}),
  },
});

const check = {
  "Проверка по местам работы": props.item.workplace,
  "Проверка документов": props.item.document,
  "Проверка задолженностей": props.item.debt,
  "Проверка банкротства": props.item.bankruptcy,
  "Проверка по БКИ": props.item.bki,
  "Проверка судебных решений": props.item.courts,
  "Проверка аффилированности": props.item.affilation,
  "Проверка по списку террористов": props.item.terrorist,
  "Проверка в открытых источниках": props.item.internet,
  "Проверка Кронос": props.item.cronos,
  "Дополнительная информация": props.item.addition,
  Комментарии: props.item.comment,
  Результат: h(UBadge, {
    color:
      props.item.conclusion === Conclusions.agreed
        ? "success"
        : props.item.conclusion === Conclusions.comments
        ? "warning"
        : props.item.conclusion === Conclusions.cancel
        ? "neutral"
        : "error",

    label: props.item.conclusion,
  }),
  "Дата записи": h(NuxtTime, {
    datetime: props.item.created,
  }),
};
</script>

<template>
  <div
    v-for="(value, key) in check"
    :key="key"
    :class="{ 'text-red-800': props.item.conclusion === Conclusions.denied }"
  >
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
