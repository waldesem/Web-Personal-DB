<script setup lang="ts">
import { Conclusions, type ItemField, type Verification } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});

const fields = [
  { key: "workplace", label: "Место работы" },
  { key: "document", label: "Документы" },
  { key: "debt", label: "Задолженности" },
  { key: "bankruptcy", label: "Банкротство" },
  { key: "bki", label: "Проверка по БКИ" },
  { key: "courts", label: "Судебные решения" },
  { key: "affilation", label: "Аффилированность" },
  { key: "terrorist", label: "Проверка списка террористов" },
  { key: "internet", label: "Проверка в открытых источниках" },
  { key: "cronos", label: "Проверка Кронос" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "comment", label: "Комментарии" },
  { key: "conclusion", label: "Заключение", slot: true },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const check = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.updated_at),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="check">
    <template v-if="props.item.conclusion" #conclusion>
      <UBadge
        :color="
          props.item.conclusion === Conclusions.agreed
            ? 'success'
            : props.item.conclusion === Conclusions.comments
              ? 'warning'
              : props.item.conclusion === Conclusions.cancel
                ? 'neutral'
                : 'error'
        "
        :label="props.item.conclusion"
      />
    </template>
  </ElementItemCard>
</template>
