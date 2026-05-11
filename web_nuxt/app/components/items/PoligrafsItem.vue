<script setup lang="ts">
import { Decisions, type ItemField, type Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результаты" },
  { key: "conclusion", label: "Заключение", slot: true },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const pfo = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.updated_at),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="pfo">
    <template v-if="props.item.conclusion" #conclusion>
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
    </template>
  </ElementItemCard>
</template>
