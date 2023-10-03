<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave, useRoute } from 'vue-router';
import { profileStore } from '@/store/profile';
import { alertStore } from '@/store/alert';
import AnketaTab from '@content/tabs/AnketaTab.vue';
import CheckTab from '@content/tabs/CheckTab.vue';
import RegistryTab from '@content/tabs/RegistryTab.vue';
import PoligrafTab from '@content/tabs/PoligrafTab.vue';
import InvestigateTab from '@content/tabs/InvestigateTab.vue';
import InquiryTab from '@content/tabs/InquiryTab.vue';

const storeAlert = alertStore();
const storeProfile = profileStore();

const route = useRoute();
storeProfile.candId = route.params.id as string;


onBeforeMount(() => {
  storeProfile.getItem('profile');
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  storeProfile.cancelEdit();
  next();
});

</script>
``
<template>
  <div class="container py-3">
    <div class="py-5">
      
      <div class="row">
        <div class="col">
          <div class="card" style="width: 18rem;">
            <img src="..." class="card-img-top" alt="...">
            <div class="card-body">
              <form @change="storeProfile.submitFile($event, 'image', storeProfile.anketa.resume['id'])">
                <div class="mb-3">
                  <input class="form-control form-control-sm" id="formImage" type="file">
                </div>
              </form>
            </div>
          </div>
        </div>
        <div class="col">
          <a href="#" @click="storeProfile.deleteFile('image', storeProfile.anketa.resume['id'])" 
            title="Удалить">
            <i class="bi bi-trash"></i>
          </a>
        </div>
      </div>

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
