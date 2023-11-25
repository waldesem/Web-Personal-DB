<script setup lang="ts">

import { defineAsyncComponent } from 'vue';

const RowDivSlot = defineAsyncComponent(() => import('@components/elements/RowDivSlot.vue'));

const props = defineProps({
  deleteItem: {
    type: Function,
    required: true
  },
  openForm: {
    type: Function,
    required: true
  },
  item: {
    type: Object,
    required: true
  }
});

</script>


<template>
  <RowDivSlot :slotOne="true" :slotTwo="true"  :print="true">
    <template v-slot:divOne>
      <a href="#" title="Удалить"
        @click="props.deleteItem(props.item['id'].toString(), 'inquiry')">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a href="#" title="Изменить"
        @click="props.openForm('inquiry', 'update', props.item['id'].toString(), props.item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Информация'" :value="props.item['info']"/>
  <RowDivSlot :label="'Иннициатор'" :value="props.item['initiator']"/>
  <RowDivSlot :label="'Источник'" :value="props.item['source']"/>
  <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']"/>
  <RowDivSlot :label="'Дата запроса'" :value="props.item['deadline']"/>        
</template>