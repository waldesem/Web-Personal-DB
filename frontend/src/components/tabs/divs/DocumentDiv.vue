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
      <a href="#" @click="props.deleteItem('document', 'delete', item['id'].toString())" title="Удалить">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a class="btn btn-link" title="Изменить"
        @click= "props.openForm('document', 'update', item['id'].toString(), item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Вид документа'" :value="item['view']"/>
  <RowDivSlot :label="'Серия'" :value="item['series']"/>
  <RowDivSlot :label="'Номер'" :value="item['number']"/>
  <RowDivSlot :label="'Кем выдан'" :value="item['agency']"/>
  <RowDivSlot :label="'Дата выдачи'" :value="new Date(String(item['issue'])).
                                              toLocaleDateString('ru-RU')"/>
</template>