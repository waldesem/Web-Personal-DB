<script setup lang="ts">

import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';
import { appAuth } from '../../store/auth';
import server from '../../store/server';
import AnketaTab from './profile/AnketaTab.vue';
import CheckTab from './profile/CheckTab.vue';
import RegistryTab from './profile/RegistryTab.vue';
import PoligrafTab from './profile/PoligrafTab.vue';
import InvestigateTab from './profile/InvestigateTab.vue';
import InquiryTab from './profile/InquiryTab.vue';
//import PhotoUpload from './profile/PhotoUpload.vue';

const storeAuth = appAuth()

const route = useRoute();

const emit = defineEmits(['updateMessage']);

const data = ref({
  candId: route.params.id.toString(), 
  resume: {},
  docums: [],
  addrs: [],
  conts: [],
  works: [],
  relate: [],
  staffs: [],
  verification: [], 
  register: [], 
  pfo: [], 
  inquisition: [], 
  needs: [], 
  status: '', 
  header: '',
  path: '',
  lastCheck: {}, 
  print: false
});

onBeforeMount(() => {
  getProfile(data.value.candId)
});


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};


async function getProfile(id=data.value.candId) {
  data.value.candId = id;
  if (id === '0') {
    updateMessage({attr: 'alert-info', text: 'Заполните форму'})
    data.value.header = 'Новая анкета'

  } else {
    const response = await storeAuth.axiosInstance.get(`${server}/profile/${id}`);
    const {resume, documents, addresses, contacts, relations, workplaces, staffs, 
      checks, registries, pfos, invs, inquiries} = response.data;

    Object.assign(data.value, {
      resume: resume,
      docums: documents,
      addrs: addresses,
      conts: contacts,
      works: workplaces,
      staffs: staffs,
      relate: relations,
      verification: checks,
      register: registries,
      pfo: pfos,
      inquisition: invs,
      needs: inquiries,
      header: resume['fullname'],
      path: resume['path'],
      status: resume['status']
    })
  }
}

</script>

<template>
  <div class="container py-3">    
    <!--div v-if="data.candId !== '0'" class="row">
      <div class="col">
        <div class="text-end">
          <button @click="data.print=true" class="btn btn-outline-secondary btn-sm">Версия для печати</button>
        </div>
      </div>
    </div-->
    
    <!--PhotoUpload v-if="data.candId !== '0'"
                :path="data.path" 
                :candId="data.candId" 
                @updateMessage="updateMessage" 
                @updateItem="getProfile" /-->
    
    <div class="py-5"><h4>{{data.header}}</h4></div>

    <div class="nav nav-tabs nav-justified" role="tablist">
      <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab">Анкета</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab">Проверки</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab">Согласования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab">Полиграф</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigateTab" type="button" role="tab">Расследования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab">Запросы</button>
    </div>
    <div class="tab-content">
      <div class="tab-pane active py-1" role="tabpanel" id="anketaTab">
        <AnketaTab :resume="data.resume" 
                   :staffs="data.staffs" 
                   :docums="data.docums" 
                   :addrs="data.addrs" 
                   :conts="data.conts" 
                   :works="data.works" 
                   :relate="data.relate" 
                   :candId="data.candId" 
                   :status="data.status"
                   @updateMessage="updateMessage" @updateItem="getProfile"/>
      </div>
      <template v-if="data.candId !== '0'">
        <div class="tab-pane py-1" role="tabpanel" id="checkTab">
          <CheckTab 
                  :table="data.verification" 
                  :candId="data.candId" 
                  :status="data.status"
                  @updateMessage="updateMessage" 
                  @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="registryTab">
          <RegistryTab 
                  :table="data.register" 
                  :candId="data.candId" 
                  @updateMessage="updateMessage" 
                  @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="poligrafTab">
          <PoligrafTab 
                  :table="data.pfo" 
                  :candId="data.candId" 
                  @updateMessage="updateMessage" 
                  @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="investigateTab">
          <InvestigateTab 
                  :table="data.inquisition" 
                  :candId="data.candId" 
                  @updateMessage="updateMessage" 
                  @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="inquiryTab">
          <InquiryTab :table="data.needs" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
      </template>
    </div>
  </div>
  <!--button v-if="data.print" @click="data.print=false" class="btn btn-outline-secondary btn-sm d-print-none">Вернуться</button-->
</template>
