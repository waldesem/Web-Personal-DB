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
      <a href="#" @click="props.deleteItem('relation', 'delete', item['id'].toString())" title="Удалить">
        <i class="bi bi-trash"></i>
      </a>
    </template>
    <template v-slot:divTwo>
      <a class="btn btn-link" title="Изменить"
        @click= "props.openForm('relation', 'update', item['id'].toString(), item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Тип связи'" :value="item['relation']"/>
  <RowDivSlot :label="'Связь'" :slotTwo="true">
    <router-link :to="{ name: 'profile', params: { group: 'staffsec', id: String(item['relation_id']) } }">
      ID #{{ item['relation_id'] }}
    </router-link>
  </RowDivSlot>
</template>