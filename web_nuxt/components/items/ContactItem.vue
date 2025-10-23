<script setup lang="ts">
import type { Contact } from '@/types';

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    required: true,
  },
});
</script>

<template>
    <ElementsLabelValue label="Вид" :value="props.item.view" />
    <ElementsLabelValue label="Контакт" :value="props.item.contact" />
</template>
