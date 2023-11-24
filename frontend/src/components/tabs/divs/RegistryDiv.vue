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
  <RowDivSlot :label="'Комментарий'" :value="props.item['comments']"/>
  <RowDivSlot :label="'Решение'" :value="props.item['decision']"/>
  <RowDivSlot :label="'Руководитель'" :value="props.item['supervisor']"/>
  <RowDivSlot :label="'Дата'" :value="new Date(String(item['deadline'])).
                                          toLocaleDateString('ru-RU')"/>
</template>