<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { profileStore } from '@/store/profile';
import { alertStore } from '@/store/alert';
import AnketaTab from '@components/tabs/AnketaTab.vue';
import CheckTab from '@components/tabs/CheckTab.vue';
import RegistryTab from '@components/tabs/RegistryTab.vue';
import PoligrafTab from '@components/tabs/PoligrafTab.vue';
import InvestigateTab from '@components/tabs/InvestigateTab.vue';
import InquiryTab from '@components/tabs/InquiryTab.vue';

const storeAlert = alertStore();
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
      <div class="py-3">
        <div class="card" style="width: 16rem;">
          <img :src="storeProfile.urlImage 
                ? storeProfile.urlImage 
                : '/no-photo.png'" 
                style="width: 100%; height: auto;" 
                class="card-img-top" alt="...">
          <div v-if="!storeProfile.printPdf" class="card-body">
            <form @change="storeProfile.submitFile($event, 'image', storeProfile.profile.resume['id'])">
              <input class="form-control form-control-sm" id="formImage" type="file">                  
            </form>
          </div>
        </div>
      </div>
      <div class="py-2">
        <h3>{{storeProfile.profile.resume['fullname']}}
          &nbsp;
          <a href="#" @click="storeProfile.printPdf = !storeProfile.printPdf;
                              storeAlert.setAlert">
            <i class="bi bi-printer" title="Версия для печати"></i>
          </a>
        </h3>
      </div>
    </div>
    <template v-if="!storeProfile.printPdf">
      <div v-if="!storeProfile.printPdf" class="nav nav-tabs nav-justified" role="tablist">
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
    </template>
    <template v-else>
      <h5>Анкета</h5>
      <AnketaTab />
      <h5>Проверки</h5>
      <CheckTab />
      <h5>Согласования</h5>
      <RegistryTab />
      <h5>Полиграф</h5>
      <PoligrafTab />
      <h5>Расследования</h5>
      <InvestigateTab />
      <h5>Запросы</h5>
      <InquiryTab />
    </template>
  </div>

</template>
