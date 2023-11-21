<script setup lang="ts">

import { defineAsyncComponent, onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { useRoute } from 'vue-router';
import { profileStore } from '@/store/profile';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const PhotoCard = defineAsyncComponent(() => import('@components/layouts/PhotoCard.vue'));
const AnketaTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const CheckTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const RegistryTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const PoligrafTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const InvestigateTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const InquiryTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const OneTab = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeProfile = profileStore();

const route = useRoute();

storeProfile.dataProfile.candId = route.params.id.toString();

const tabsObject = {
  anketaTab: ['Анкета', AnketaTab],
  сheckTab: ['Проверки', CheckTab],
  registryTab: ['Согласования', RegistryTab],
  poligrafTab: ['Полиграф', PoligrafTab],
  investigateTab: ['Расследования', InvestigateTab],
  inquiryTab: ['Запросы', InquiryTab],
  oneTab: ['1C', OneTab]
};

onBeforeMount(async () => {
  Promise.all([
    await storeProfile.dataProfile.getProfile(),
    await storeProfile.dataProfile.getImage()
  ])
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  storeProfile.dataProfile.cancelEdit();
  storeProfile.dataProfile.url = '';
  storeProfile.dataProfile.candId = '';
  next();
});

</script>

<template>
  <div class="container py-3">
    
    <PhotoCard :url="storeProfile.dataProfile.url"
               :param="['image', storeProfile.dataProfile.resume.id]"
               :func="storeProfile.dataProfile.submitFile"/>

    <HeaderDiv :page-header="storeProfile.dataProfile.resume['fullname']" />

    <div class="nav nav-tabs nav-justified" role="tablist">
      <button v-for="(value, key) in tabsObject" :key="key"
              class="nav-link active" type="button" role="tab" 
              data-bs-toggle="tab" :data-bs-target="`#${key}`">
        {{value[0]}}
      </button>
    </div>

    <div class="tab-content">
      <div v-for="(value, key) in tabsObject" :key="key" :id="key"
          class="tab-pane fade py-1" role="tabpanel" 
          :class="key === 'anketaTab' ? 'show active' : ''" >
        <component :is="value[1]"></component>
      </div>
    </div>

    <router-link :to="{ name: 'print' }">
      <i class="bi bi-printer fs-1" title="Версия для печати"></i>
    </router-link>

  </div>
</template>

<style scoped>
.bi-printer {
  position: fixed;
  top: 80px;
  right: 40px;
  z-index: 9999;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
}
</style>
