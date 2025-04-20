<script setup lang="ts">
import type { Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
});
</script>

<template>
  <ElementsLabelSlot :label="'Тема проверки'">{{
    props.item.theme
  }}</ElementsLabelSlot>
  <ElementsLabelSlot :label="'Результат'">{{
    props.item.results
  }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Заключение'">
    <UBadge
      :color="
        props.item.conclusion === 'БЕЗ ЗАМЕЧАНИЙ'
          ? 'success'
          : props.item.conclusion === 'С КОММЕНТАРИЯМИ'
          ? 'primary'
          : 'error'
      "
      :label="props.item.conclusion"
      variant="soft"
    />
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.item.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
</template>