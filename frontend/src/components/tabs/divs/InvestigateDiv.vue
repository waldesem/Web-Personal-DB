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
  submitFile: {
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
      <a href="#" title="Удалить"
        @click="props.deleteItem(props.item['id'].toString(), 'investigation')">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a href="#" title="Изменить"
         @click="props.openForm('investigation', 'update', props.item['id'].toString(), props.item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Тема'" :value="props.item['theme']"/>
  <RowDivSlot :label="'Информация'" :value="props.item['info']"/>
  <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']"/>
  <RowDivSlot :label="'Дата'" :value="new Date(String(item['deadline'])).
                                          toLocaleDateString('ru-RU')"/>
  <RowDivSlot :slotOne="true">
    <form class="form" enctype="multipart/form-data" role="form" 
          @change="props.submitFile($event, 'investigation', item['id'].toString())">
      <input class="form-control" id="file" type="file" ref="file" multiple>
    </form>
  </RowDivSlot>
</template>