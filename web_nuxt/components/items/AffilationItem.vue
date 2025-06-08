<script setup lang="ts">
import type { Affilation } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    default: () => ({}),
  },
});

const affilation = {
  "Тип участия": props.item.view,
    Организация: props.item.organization,
    ИНН: props.item.inn,
};
</script>

<template>
  <div v-for="(value, key) in affilation" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
