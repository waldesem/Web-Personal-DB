<script setup lang="ts">

import axios from 'axios';
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import config from '@/config';
import NavBar from './NavBar.vue';
import AlertMessage from './AlertMessage.vue';
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
  resums: '',
  docums: '',
  addrs: '',
  conts: '',
  works: '',
  relate: [],
  staffs: '',
  verification: '', 
  register: '', 
  pfo: '', 
  inquisition: '', 
  needs: '', 
  status: '', 
  header: '',
  resume: {}, 
  lastCheck: {}, 
  print: false
});

const resume_labels = [
  'id', 'Категория', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 
  'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Создан', 'Обновлен', 'Внешний id'
];
const staff_labels =  ['id', 'Должность', 'Департамент'];
const docs_labels = ['id', 'Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'];
const addr_labels = ['id', 'Тип', 'Регион', 'Адрес'];
const cont_labels = ['id', 'Вид', 'Контакт'];
const work_labels = ['id', 'Период', 'Организация', 'Адрес', 'Должность'];
const check_labels = [
  'id', 'Проверка по местам работы', 'Бывший работник МТСБ', 'Проверка паспорта', 'Проверка ИНН', 
  'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 'Проверка судебных дел', 
  'Проверка аффилированности', 'Проверка в списке террористов', 'Проверка нахождения в розыске', 
  'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 'Дополнительная информация', 
  'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 'Дата проверки', 'Сотрудник СБ'
];
const registry_labels = ['id', 'Комментарий', 'Решение', 'Дата', 'Согласующий'];
const poligraf_labels = ['id', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
const investigation_labels = ['id', 'Тема', 'Информация', 'Дата проверки'];
const inquiry_labels = ['id', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];

const print_headers = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Места работы', 
                      'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы' ];

function updateMessage(alert: Object) {
  data.value.attr = (alert as { attr: string })["attr"];
  data.value.text = (alert as { text: string })["text"];
}

async function getProfile(id=data.value.candId) {
  data.value.candId = id;
  if (id === '0') {
    updateMessage({attr: 'alert-info', text: 'Заполните форму'})
    data.value.header = 'Новая анкета'
  } else {
    const response = await axios.get(`${config.appUrl}/profile/${id}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const {resume, documents, addresses, contacts, relations, workplaces, staffs, checks, registries, pfos, invs, inquiries} = response.data;
    Object.assign(data.value, {
      resums: createItemTable(resume_labels, resume),
      docums: createItemTable(docs_labels, documents),
      addrs: createItemTable(addr_labels, addresses),
      conts: createItemTable(cont_labels, contacts),
      works: createItemTable(work_labels, workplaces),
      staffs: createItemTable(staff_labels, staffs),
      relate: relations,
      verification: createItemTable(check_labels, checks),
      register: createItemTable(registry_labels, registries),
      pfo: createItemTable(poligraf_labels, pfos),
      inquisition: createItemTable(investigation_labels, invs),
      needs: createItemTable(inquiry_labels, inquiries),
      header: resume[0]['fullname'],
      status: resume[0]['status'],
      resume: resume[0],
      lastCheck: checks[0]
    })
  }
}

function createItemTable(names: string[], response: Array<Object>) {
  if (!response.length) {
    return `<p>Данные отсутствуют</p>`;
  }
  const rows = response.map((item) => {
    return names.map((name, i) => {
      if (Object.keys(item)[i] === 'create' || 
          Object.keys(item)[i] === 'update' || 
          Object.keys(item)[i] === 'birthday' || 
          Object.keys(item)[i] === 'deadline') {
        
        if (Object.values(item)[i] != null) {
          const date = new Date(String(Object.values(item)[i]));
          return `<tr>
            <td width="25%">${name}</td>
            <td>${date.toLocaleDateString('ru-RU')}</td>
            </tr>`;
        }
      } else if (Object.keys(item)[i] === 'id' ) {
        return `<thead><tr>
          <th colspan="2">${name} #${Object.values(item)[i]}</th>
          </tr></thead>`;
      
      } else if (Object.keys(item)[i] === 'path' ) {
        return `<tr>
          <td width="25%">${name}</td>
          <td><a href="${Object.values(item)[i]}">Открыть</a></td>
          </tr>`;
      
      } else if (Object.keys(item)[i] === 'relation_id' ) {
        return `<tr>
          <td width="25%">${name}</td>
          <td><router-link :to="{ name: 'profile', params: {id: ${Object.values(item)[i]}} }">ID #${Object.values(item)[i]}</router-link>
            </td>
            </tr>`;
      
      } else if (Object.values(item)[i] === null) {
        return `<tr>
          <td width="25%">${name}</td>
          <td>${''}</td>
          </tr>`;
      
      } else {
        return `<tr>
          <td width="25%">${name}</td>
          <td>${Object.values(item)[i]}</td>
          </tr>`;
      }
    }).join('');
  });
  const body = `<tbody>${rows.join('')}</tbody>`;
  return `<table class="table table-responsive">${body}</table>`
}

onBeforeMount(() => {
  getProfile(data.value.candId)
});

</script>

<template>
  <template v-if="!data.print">
    <NavBar />
    <div class="container py-3">
      <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
      <div v-if="data.candId !== '0'" class="row">
        <div class="col">
          <div class="text-end">
            <button @click="data.print=true" class="btn btn-outline-secondary btn-sm">Версия для печати</button>
          </div>
        </div>
      </div>
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
    <FooterDiv />
  </template>
  <template v-else >
    <div class="container py-3">
      <div class="py-2"><h4>{{data.header}}</h4></div>  
      <div v-for="(elem, index) in [data.resums, data.staffs, data.docums, data.addrs, data.conts, data.works, 
                           data.verification, data.register, data.pfo, data.inquisition, data.needs]">
        <p>{{ print_headers[index] }}</p>
        <div v-if="elem!=='<p>Данные отсутствуют</p>'" class="py-2" v-html="elem ? elem : ''"></div>
      </div>
    <button @click="data.print=false" class="btn btn-outline-secondary btn-sm d-print-none">Вернуться</button>
  </div>
  </template>
</template>