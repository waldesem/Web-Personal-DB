<script setup lang="ts">

import { defineAsyncComponent } from 'vue';

const RowDivSlot = defineAsyncComponent(() => import('@components/elements/RowDivSlot.vue'));

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
});

</script>


<template>
  <RowDivSlot :label="'Начало работы'" :value="props.item['start_date']"/>
  <RowDivSlot :label="'Окончание работы'" :value="props.item['end_date']"/>
  <RowDivSlot :label="'Стартовая должность'" :value="props.item['start_position']"/>
  <RowDivSlot :label="'Должность при увольнении'" :value="props.item['end_position']"/>
</template>