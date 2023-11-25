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
  getItem: {
    type: Function,
    required: true
  },
  item: {
    type: Object,
    required: true
  },
  regions: {
    type: Object,
    required: true
  }
});

</script>

<template>
  <RowDivSlot :slotOne="true" :slotTwo="true" :print="true">
    <template v-slot:divOne>
      <a href="#" title="Изменить"
         @click="props.openForm('resume', 'update', props.item['id'], props.item)">
        <i class="bi bi-pencil-square"></i>
      </a>
    </template>
  </RowDivSlot>
  <RowDivSlot :label="'Категория'" :value="props.item['category']"/>
  <RowDivSlot :label="'Регион'" :slotTwo="true">
    <a href="#" data-bs-toggle="modal" data-bs-target="#modalRegion"
       @click="props.openForm('resume', 'location', props.item['id'], props.item)">
        {{ props.regions[props.item['region_id']] }}
    </a>
  </RowDivSlot>
  <RowDivSlot :label="'Фамилия Имя Отчество'" :value="props.item['fullname']"/>
  <RowDivSlot :label="'Изменение имени'" :value="props.item['previous']"/>
  <RowDivSlot :label="'Дата рождения'" :value="props.item['birthday']"/>
  <RowDivSlot :label="'Место рождения'" :value="props.item['birthplace']"/>
  <RowDivSlot :label="'Гражданство'" :value="props.item['country']"/>
  <RowDivSlot :label="'Второе гражданство'" :value="props.item['ext_country']"/>
  <RowDivSlot :label="'СНИЛС'" :value="props.item['snils']"/>
  <RowDivSlot :label="'ИНН'" :value="props.item['inn']"/>
  <RowDivSlot :label="'Образование'" :value="props.item['education']"/>
  <RowDivSlot :label="'Дополнительная информация'" :value="props.item['addition']"/>
  <RowDivSlot :label="'Материалы'" :value="props.item['path']" :slotTwo="true" :print="true">
    <router-link :to="{name: 'manager', params: {group: 'staffsec', path: props.item['path'].split('/')}}">
      {{ props.item['path'] }}
    </router-link>
  </RowDivSlot>
  <RowDivSlot :label="'Статус'" :slotTwo="true">
    <a href="#" @click="props.getItem('resume', 'status', props.item['id'])">
      {{ props.item['status'] }}
    </a>
  </RowDivSlot>
  <RowDivSlot :label="'Создан'" :value="new Date(String(props.item['create'])).
                                              toLocaleDateString('ru-RU')"/>
  <RowDivSlot :label="'Обновлен'" :value="new Date(String(props.item['update'])).
                                              toLocaleDateString('ru-RU')"/>
  <RowDivSlot :label="'Внешний ID'" :value="props.item['request_id']"/>
</template>
