<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { profileStore } from '@/store/profile';
import AnketaTab from '@components/tabs/AnketaTab.vue';
import CheckTab from '@components/tabs/CheckTab.vue';
import RegistryTab from '@components/tabs/RegistryTab.vue';
import PoligrafTab from '@components/tabs/PoligrafTab.vue';
import InvestigateTab from '@components/tabs/InvestigateTab.vue';
import InquiryTab from '@components/tabs/InquiryTab.vue';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';
import PhotoCard from '@components/layouts/PhotoCard.vue';

const storeProfile = profileStore();

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
    <div class="py-1">
      <PhotoCard />
      <HeaderDiv :page-header="storeProfile.profile.resume['fullname']" />
      &nbsp;
      <router-link :to="{ name: 'print' }">
        <i class="bi bi-printer" title="Версия для печати"></i>
      </router-link>
    </div>
    <div class="nav nav-tabs nav-justified" role="tablist">
      <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" 
          type="button" role="tab">Анкета</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" 
          type="button" role="tab">Проверки</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" 
          type="button" role="tab">Согласования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" 
          type="button" role="tab">Полиграф</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigateTab" 
          type="button" role="tab">Расследования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" 
          type="button" role="tab">Запросы</button>
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
  </div>
</template>
