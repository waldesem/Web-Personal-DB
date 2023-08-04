<script setup lang="ts">

import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';
import config from '../config';
import NavBar from './NavBar.vue';
import AlertMessage from './AlertMessage.vue';
import PhotoUpload from './profile/PhotoUpload.vue';
import AnketaTab from './profile/AnketaTab.vue';
import CheckTab from './profile/CheckTab.vue';
import RegistryTab from './profile/RegistryTab.vue';
import PoligrafTab from './profile/PoligrafTab.vue';
import InvestigateTab from './profile/InvestigateTab.vue';
import InquiryTab from './profile/InquiryTab.vue';
import FooterDiv from './FooterDiv.vue';

const route = useRoute();

const data = ref({
  candId: String(route.params.id), 
  attr: '', 
  text: '',
  resums: [],
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
  resume: {}, 
  lastCheck: {}, 
  print: false
});

onBeforeMount(() => {
  getProfile(data.value.candId)
});


function updateMessage(alert: Object) {
  data.value.attr = (alert as { attr: string })["attr"];
  data.value.text = (alert as { text: string })["text"];
}


async function getProfile(id=data.value.candId) {
  data.value.candId = id;
  if (id === '0') {
    updateMessage({attr: 'alert-info', text: 'Заполните форму'})
    data.value.header = 'Новая анкета'
    return
  } else {
    const response = await axios.get(`${config.appUrl}/profile/${id}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const {resume, documents, addresses, contacts, relations, workplaces, staffs, 
      checks, registries, pfos, invs, inquiries} = response.data;

    Object.assign(data.value, {
      resums: resume,
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
      header: resume[0]['fullname'],
      path: resume[0]['path'],
      status: resume[0]['status'],
      resume: resume[0],
      lastCheck: checks[0]
    })
  }
}

</script>

<template>
  <NavBar />
  <div class="container py-5">
    
    <AlertMessage v-if="data.attr || !data.print" :attr="data.attr" :text="data.text" />
    
    <div v-if="data.candId !== '0'" class="row">
      <div class="col">
        <div class="text-end">
          <button @click="data.print=true" class="btn btn-outline-secondary btn-sm">Версия для печати</button>
        </div>
      </div>
    </div>
    
    <PhotoUpload v-if="data.candId !== '0'" :path="data.path" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
    
    <div v-if="data.candId === '0'" class="py-1"><h4>Создать анкету</h4></div>
    <div v-else class="py-5"><h4>{{data.header}}</h4></div>
    
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
        <AnketaTab :table="[data.resums, data.staffs, data.docums, data.addrs, data.conts, data.works]" 
        :relation="data.relate" :candId="data.candId" :resume="data.resume" :status="data.status"
        @updateMessage="updateMessage" @updateItem="getProfile"/>
      </div>
      <template v-if="data.candId !== '0'">
        <div class="tab-pane py-1" role="tabpanel" id="checkTab">
          <CheckTab :table="data.verification" :candId="data.candId" :item="data.lastCheck" :status="data.status"
          @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="registryTab">
          <RegistryTab :table="data.register" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="poligrafTab">
          <PoligrafTab :table="data.pfo" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="investigateTab">
          <InvestigateTab :table="data.inquisition" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="inquiryTab">
          <InquiryTab :table="data.needs" :candId="data.candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
      </template>
    </div>
  </div>
  <FooterDiv v-if="!data.print" />
  <button v-if="data.print" @click="data.print=false" class="btn btn-outline-secondary btn-sm d-print-none">Вернуться</button>
</template>
