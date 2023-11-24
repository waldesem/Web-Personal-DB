<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const RowDivSlot = defineAsyncComponent(() => import('@components/elements/RowDivSlot.vue'));
const ResumeDiv = defineAsyncComponent(() => import('@components/tabs/divs/ResumeDiv.vue'));
const StaffDiv = defineAsyncComponent(() => import('@components/tabs/divs/StaffDiv.vue'));
const DocumentDiv = defineAsyncComponent(() => import('@components/tabs/divs/DocumentDiv.vue'));
const AddressDiv = defineAsyncComponent(() => import('@components/tabs/divs/AddressDiv.vue'));
const ContactDiv = defineAsyncComponent(() => import('@components/tabs/divs/ContactDiv.vue'));
const RelationDiv = defineAsyncComponent(() => import('@components/tabs/divs/RelationDiv.vue'));
const WorkplaceDiv = defineAsyncComponent(() => import('@components/tabs/divs/WorkplaceDiv.vue'));
const AffilationDiv = defineAsyncComponent(() => import('@components/tabs/divs/AffilationDiv.vue'));

const storeProfile = profileStore();
const storeClassify = classifyStore();

</script>

<template>
  <div class="container">
    <div class="text-secondary text-end text-opacity-85 py-3">
      <h6>Для служебного пользования</h6>
    </div>
    <div class="card" style="width: 16rem;">
      <img :src="storeProfile.dataProfile.url ? storeProfile.dataProfile.url : '/no-photo.png'" 
            style="width: 100%; height: auto;" class="card-img-top" alt="...">
    </div>
    <HeaderDiv :page-header="storeProfile.dataProfile.resume['fullname']" />

    <ResumeDiv v-if="storeProfile.dataProfile.resume"
                    :item="storeProfile.dataProfile.resume"
                    :regions="storeClassify.classData.regions"
                    :deleteItem="storeProfile.dataProfile.deleteItem"
                    :openForm="storeProfile.dataProfile.openForm"
                    :getItem="storeProfile.dataProfile.getItem"/>    

    <h6>Должности</h6>
    <div v-if="storeProfile.dataProfile.staffs" class="py-2">
      <div v-for="item in storeProfile.dataProfile.staffs" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>
          <StaffDiv :item="item"
                    :deleteItem="storeProfile.dataProfile.deleteItem"
                    :openForm="storeProfile.dataProfile.openForm"/>
      </div>
    </div>

    <h6>Документы</h6>
    <div v-if="storeProfile.dataProfile.docums" class="py-2">
      <div v-for="item in storeProfile.dataProfile.docums" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>
          <DocumentDiv :item="item"
                       :deleteItem="storeProfile.dataProfile.deleteItem"
                       :openForm="storeProfile.dataProfile.openForm"/>
      </div>
    </div>

    <h6>Адреса</h6>
    <div v-if="storeProfile.dataProfile.addrs" class="py-2">
      <div v-for="item in storeProfile.dataProfile.addrs" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>
          <AddressDiv :item="item"
                      :deleteItem="storeProfile.dataProfile.deleteItem"
                      :openForm="storeProfile.dataProfile.openForm"/>    
      </div>
    </div>

    <h6>Контакты</h6>
    <div v-if="storeProfile.dataProfile.conts" class="py-2">
      <div v-for="item in storeProfile.dataProfile.conts" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>      
          <ContactDiv :item="item"
                      :deleteItem="storeProfile.dataProfile.deleteItem"
                      :openForm="storeProfile.dataProfile.openForm"/> 
      </div>
    </div>

    <h6>Работа</h6>
    <div v-if="storeProfile.dataProfile.works" class="py-2">
      <div v-for="item in storeProfile.dataProfile.works" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>      
          <WorkplaceDiv :item="item"
                        :deleteItem="storeProfile.dataProfile.deleteItem"
                        :openForm="storeProfile.dataProfile.openForm"/>
      </div>
    </div>

    <h6>Аффилированность</h6>
    <div v-if="storeProfile.dataProfile.affilation" class="py-2">
      <div v-for="item in storeProfile.dataProfile.affilation" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>
          <AffilationDiv :item="item"
                         :deleteItem="storeProfile.dataProfile.deleteItem"
                         :openForm="storeProfile.dataProfile.openForm"/>
      </div>
    </div>

    <h6>Связи</h6>
    <div v-if="storeProfile.dataProfile.staffs" class="py-2">
      <div v-for="item in storeProfile.dataProfile.staffs" :key="item['id']">
        <RowDivSlot :label="'ID'" :value="item['id']"/>      
          <RelationDiv :item="item"
                       :deleteItem="storeProfile.dataProfile.deleteItem"
                       :openForm="storeProfile.dataProfile.openForm"/>
      </div>
    </div>
    <h6>Проверки</h6>
    <h6>Согласования</h6>
    <h6>Полиграф</h6>
    <h6>Расследования</h6>
    <h6>Запросы</h6>
    <h6>1С</h6>
  </div>
</template>