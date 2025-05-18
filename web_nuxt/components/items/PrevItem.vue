<script setup lang="ts">
import type { Previous } from "@/types";

const props = defineProps({
  item: {
    type: Object as () => Previous,
    default: () => ({}),
  }
})
</script>

<template>
  <ElementsLabelSlot :label="'Фамилия'">
    {{ props.item.surname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Имя'">
    {{ props.item.firstname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="item['patronymic']" :label="'Отчество'">
    {{ props.item.patronymic }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="item['changed']" :label="'Год изменения'">
    {{ props.item.changed }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="item['reason']" :label="'Причина'">
    {{ props.item.reason }}
  </ElementsLabelSlot>
</template>
