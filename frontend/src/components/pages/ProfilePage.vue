<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { useRoute } from 'vue-router';
import { profileStore } from '@/store/profile';

const AnketaTab = () => import('@components/tabs/AnketaTab.vue');
const CheckTab = () => import('@components/tabs/CheckTab.vue');
const RegistryTab = () => import('@components/tabs/RegistryTab.vue');
const PoligrafTab = () => import('@components/tabs/PoligrafTab.vue');
const InvestigateTab = () => import('@components/tabs/InvestigateTab.vue');
const InquiryTab = () => import('@components/tabs/InquiryTab.vue');
const HeaderDiv = () => import('@components/layouts/HeaderDiv.vue');
const PhotoCard = () => import('@components/layouts/PhotoCard.vue');

const storeProfile = profileStore();

const route = useRoute();

storeProfile.candId = route.params.id.toString();

const tabsObject = {
  anketaTab: ['Анкета', AnketaTab],
  сheckTab: ['Проверки', CheckTab],
  registryTab: ['Согласования', RegistryTab],
  poligrafTab: ['Полиграф', PoligrafTab],
  investigateTab: ['Расследования', InvestigateTab],
  inquiryTab: ['Запросы', InquiryTab]
};

onBeforeMount(async () => {
  Promise.all([
      await getProfile(),
      await storeProfile.getImage()
  ])
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  storeProfile.cancelEdit();
  storeProfile.urlImage = '';
  storeProfile.candId = '';
  next();
});

async function getProfile() {
  await Promise.all([
    [
      'resume', 
      'staff', 
      'document', 
      'address',
      'contact', 
      'workplace', 
      'relation', 
      'check', 
      'registry', 
      'poligraf', 
      'investigation', 
      'inquiry'
    ].map(async (item) => await storeProfile.getItem(item))
  ]);
};

</script>

<template>
  <div class="container py-3">
    <PhotoCard :profileId="storeProfile.profile.resume['id']" :imageUrl="storeProfile.urlImage"/>
    <HeaderDiv :page-header="storeProfile.profile.resume['fullname']" />
    <div class="nav nav-tabs nav-justified" role="tablist">
      <button v-for="(value, key) in tabsObject" :key="key"
              class="nav-link active" type="button" role="tab" 
              data-bs-toggle="tab" :data-bs-target="`#${key}`">
        {{value[0]}}
      </button>
    </div>
    <div class="tab-content">
      <div class="tab-pane fade show active py-1" role="tabpanel" id="anketaTab">
        <AnketaTab />
      </div>
      <div class="tab-pane fade py-1" role="tabpanel" id="checkTab">
        <CheckTab />
      </div>
      <div class="tab-pane fade py-1" role="tabpanel" id="registryTab">
        <RegistryTab />
      </div>
      <div class="tab-pane fade py-1" role="tabpanel" id="poligrafTab">
        <PoligrafTab />
      </div>
      <div class="tab-pane fade py-1" role="tabpanel" id="investigateTab">
        <InvestigateTab />
      </div>
      <div class="tab-pane fade py-1" role="tabpanel" id="inquiryTab">
        <InquiryTab />
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
