<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { appProfile } from '@/store/profile';
import { appAlert } from '@/store/alert';
import AnketaTab from '@content/tabs/AnketaTab.vue';
import CheckTab from '@content/tabs/CheckTab.vue';
import RegistryTab from '@content/tabs/RegistryTab.vue';
import PoligrafTab from '@content/tabs/PoligrafTab.vue';
import InvestigateTab from '@content/tabs/InvestigateTab.vue';
import InquiryTab from '@content/tabs/InquiryTab.vue';
//import PhotoForm from '@content/forms/PhotoForm.vue';

const storeAlert = appAlert();
const storeProfile = appProfile();
const route = useRoute();
storeProfile.candId = route.params.id as string;


onBeforeMount(() => {
  storeProfile.getProfile();
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  storeProfile.cancelEdit();
  next();
});

</script>
``
<template>
  <div class="container py-5">
    <div class="py-5">
      <!-- <PhotoForm /> -->
      <h4>{{storeProfile.anketa.resume['fullname']}}
        &nbsp;
        <a href="#" @click="storeProfile.printPdf = !storeProfile.printPdf;
                            storeAlert.alertAttr=''; storeAlert.alertText=''">
          <i class="bi bi-printer" title="Версия для печати"></i>
        </a>
      </h4>
    </div>
    <template v-if="!storeProfile.printPdf">
      <div v-if="!storeProfile.printPdf" class="nav nav-tabs nav-justified" role="tablist">
        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab">Анкета</button>
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab">Проверки</button>
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab">Согласования</button>
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab">Полиграф</button>
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigateTab" type="button" role="tab">Расследования</button>
        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab">Запросы</button>
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

<style>

  @media print {
    .no-print {
      display: none !important;
    }
  }

</style>