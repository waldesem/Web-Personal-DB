<script setup lang="ts">
import type { Verification } from "@/types";

const UBadge = resolveComponent("UBadge");

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
        props.item.conclusion === "СОГЛАСОВАНО"
          ? "success"
          : props.item.conclusion === "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
          ? "primary"
          : props.item.conclusion === "СНЯТ С ПРОВЕРКИ"
          ? "warning"
          : "error",

      label: props.item.conclusion,
    }),
    "Дата записи": props.item.created
      ? new Date(props.item.created).toLocaleString("ru-RU")
      : "",
};
</script>

<template>
  <div v-for="(value, key) in check" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
