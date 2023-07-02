<template>
  <NavBar />
  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>{{data.fullname}}</h4></div>  
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
        <AnketaTab :table="data.questionary" :candId="data.candId" :resume="data.resume" :status="data.status" :state="data.condition" @updateMessage="updateMessage" @updateItem="getProfile"/>
      </div>
        <div class="tab-pane py-1" role="tabpanel" id="checkTab">
          <CheckTab :table="data.verification" :candId="data.candId" :item="data.lastCheck" :status="data.status" :state="data.condition" @updateMessage="updateMessage" @updateItem="getProfile" />
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
    </div>
  </div>
</template>


<script setup lang="ts">

import axios from 'axios';
import { ref, onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import appUrl from '@/config';
import NavBar from './NavBar.vue';
import AlertMessage from './AlertMessage.vue';
import AnketaTab from './profile/AnketaTab.vue';
import CheckTab from './profile/CheckTab.vue';
import RegistryTab from './profile/RegistryTab.vue';
import PoligrafTab from './profile/PoligrafTab.vue';
import InvestigateTab from './profile/InvestigateTab.vue';
import InquiryTab from './profile/InquiryTab.vue';

const route = useRoute();
const data = ref({
  attr: '', 
  text: '', 
  candId: String(route.params.id), 
  questionary: [], 
  resume: {}, 
  verification: '', 
  lastCheck: {}, 
  register: '', 
  pfo: '', 
  inquisition: '', 
  needs: '', 
  status: '', 
  condition: {}, 
  fullname: ''
});

const anketa_labels = [
  ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 
  'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Создан', 'Обновлен', 'Рекрутер', 'Внешний id'],
  ['Должность', 'Департамент'],
  ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
  ['Тип', 'Регион', 'Адрес'],
  ['Вид', 'Контакт'],
  ['Период', 'Организация', 'Адрес', 'Должность']
];
const check_labels = [
  'ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ', 
  'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 
  'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов', 
  'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 
  'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 
  'Дата проверки', 'Сотрудник СБ'
];
const registry_labels = ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'];
const poligraf_labels = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
const investigation_labels = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
const inquiry_labels = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];

onBeforeMount(() => {
  getProfile(data.value.candId)
});

function updateMessage (value: any){
  Object.assign(data.value, {
    attr: value["attr"],
    text: value["text"]
  })
}

async function getProfile(id: string) {
  data.value.candId = id;
  if (id === '0') {
    Object.assign(data.value, {
      attr: 'alert-info',
      text: 'Заполните форму',
      fullname: 'Новая анкета'
    })
    return;

  } else {
    const response = await axios.get(`${appUrl}/profile/${id}`, {
      headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`}
    });
    const [anketa, check, registry, poligraf, investigation, inquiry, state] = response.data;
    Object.assign(data.value, {
      questionary: anketa_labels.map((labels: string[], i: number) => `
        <div>${createItemTable(labels, anketa[i])}</div>
      `),
      fullname: anketa[0][0]['fullname'],
      status: anketa[0][0]['status'],
      condition: state,
      resume: anketa[0][0],
      lastCheck: check[0],
      verification: createItemTable(check_labels, check),
      register: createItemTable(registry_labels, registry),
      pfo: createItemTable(poligraf_labels, poligraf),
      inquisition: createItemTable(investigation_labels, investigation),
      needs: createItemTable(inquiry_labels, inquiry)
    })
  }
}

function createItemTable(names: string[], response: Array<Array<Object>>) {
  if (!response.length) {
    return `<p>Данные отсутствуют</p>`;
  }
  const rows = response.map((item) => {
    return names.map((name, i) => {
      if (Object.keys(item)[i] === 'create' || Object.keys(item)[i] === 'update' || Object.keys(item)[i] === 'birthday') {
        if (Object.values(item)[i] != null) {
          const date = new Date(String(Object.values(item)[i]));
          return `<tr><td width="25%">${name}</td><td>${date.toLocaleDateString('ru-RU')}</td></tr>`;
        }
      } else if (Object.keys(item)[i] === 'id' ) {
        return `<tr height="50px"><th colspan="2">${name} #${Object.values(item)[i]}</th></tr>`;
      } else if (Object.keys(item)[i] === 'path' ) {
        return `<tr><td width="25%">${name}</td><td><a href="${Object.values(item)[i]}">Открыть</a></td></tr>`;
      } else if (Object.values(item)[i] === null) {
        return `<tr><td width="25%">${name}</td><td>${''}</td></tr>`;
      } else {
        return `<tr><td width="25%">${name}</td><td>${Object.values(item)[i]}</td></tr>`;
      }
    }).join('');
  });
  const body = `<tbody>${rows.join('')}</tbody>`;
  return `<table class="table table-responsive">${body}</table>`
}

</script>
