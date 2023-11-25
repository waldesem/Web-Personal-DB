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
  <RowDivSlot :slotOne="true" :slotTwo="true" :print="true">
    <template v-slot:divOne>
      <a href="#" @click="props.deleteItem('address', 'delete', item['id'].toString())" title="Удалить">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a class="btn btn-link" title="Изменить"
        @click= "props.openForm('address', 'update', item['id'].toString(), item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Тип'" :value="item['view']"/>
  <RowDivSlot :label="'Регион'" :value="item['region']"/>
  <RowDivSlot :label="'Адрес'" :value="item['address']"/>
</template>