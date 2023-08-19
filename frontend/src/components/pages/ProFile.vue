<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import { appProfile } from '@/store/profile';
import AnketaTab from '@content/tabs/AnketaTab.vue';
import CheckTab from '@content/tabs/CheckTab.vue';
import RegistryTab from '@content/tabs/RegistryTab.vue';
import PoligrafTab from '@content/tabs/PoligrafTab.vue';
import InvestigateTab from '@content/tabs/InvestigateTab.vue';
import InquiryTab from '@content/tabs/InquiryTab.vue';
//import PhotoTab from '@content/tabs/PhotoTab.vue';

const route = useRoute();

const storeProfile = appProfile();

storeProfile.candId = route.params.id.toString();

onBeforeMount(() => {
  storeProfile.getProfile();
});

</script>

<template>
  <div class="container py-3">    
    <div class="py-5"><h4>{{storeProfile.header}}</h4></div>

    <div class="nav nav-tabs nav-justified" role="tablist">
      <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab">Анкета</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab">Проверки</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab">Согласования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab">Полиграф</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigateTab" type="button" role="tab">Расследования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab">Запросы</button>
      <!--button class="nav-link" data-bs-toggle="tab" data-bs-target="#photoTab" type="button" role="tab">Фото</button-->
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
      <!--div class="tab-pane py-1" role="tabpanel" id="photoTab">
        <PhotoTab />
      </div-->
    </div>
  </div>

</template>
