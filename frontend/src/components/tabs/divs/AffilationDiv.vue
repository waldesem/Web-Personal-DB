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
  <RowDivSlot :slotOne="true" :slotTwo="true" class="d-print-none">
    <template v-slot:divOne>
      <a href="#" @click="props.deleteItem('affilation', 'delete', item['id'].toString())" title="Удалить">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a class="btn btn-link" title="Изменить"
        @click= "props.openForm('affilation', 'update', item['id'].toString(), item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Тип участия'" :value="item['view']"/>
  <RowDivSlot :label="'Организация'" :value="item['name']"/>
  <RowDivSlot :label="'ИНН'" :value="item['inn']"/>
  <RowDivSlot :label="'Должность'" :value="item['position']"/>
  <RowDivSlot :label="'Дата декларации'" :value="new Date(item['deadline']).toLocaleDateString('ru-RU')"/>
</template>