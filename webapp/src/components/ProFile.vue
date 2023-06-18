<template>
  <NavBar />
  <div class="container py-5">
    <AlertMessage v-if="attr" :attr="attr" :text="text" />
    <div class="py-3">
      <h5>{{ fullname }}</h5>
    </div>  
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
        <AnketaTab :table="questionary" :candId="candId" :resume="resume" :status="status" :state="condition" @updateMessage="updateMessage" @updateItem="getProfile"/>
      </div>
        <div class="tab-pane py-1" role="tabpanel" id="checkTab">
          <CheckTab :table="verification" :candId="candId" :item="lastCheck" :status="status" :state="condition" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="registryTab">
          <RegistryTab :table="register" :candId="candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="poligrafTab">
          <PoligrafTab :table="pfo" :candId="candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="investigateTab">
          <InvestigateTab :table="inquisition" :candId="candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="inquiryTab">
          <InquiryTab :table="needs" :candId="candId" @updateMessage="updateMessage" @updateItem="getProfile" />
        </div>
    </div>
  </div>
</template>


<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import NavBar from './NavBar.vue';
import AlertMessage from './AlertMessage.vue';
import AnketaTab from './profile/AnketaTab.vue';
import CheckTab from './profile/CheckTab.vue';
import RegistryTab from './profile/RegistryTab.vue';
import PoligrafTab from './profile/PoligrafTab.vue';
import InvestigateTab from './profile/InvestigateTab.vue';
import InquiryTab from './profile/InquiryTab.vue';

const route = useRoute();
const attr = ref('');
const text = ref('');
const candId = ref(String(route.params.id));
const questionary = ref(['']);
const resume = ref({});
const verification = ref('');
const lastCheck = ref({});
const register = ref('');
const pfo = ref('');
const inquisition = ref('');
const needs = ref('');
const status = ref('');
const condition = ref({});
const fullname = ref('');
const anketa_labels = [
  ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 
  'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Дата', 'Рекрутер', 'Внешний id'],
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

getProfile(candId.value);

function updateMessage (data: any){
  attr.value = data["attr"];
  text.value = data["text"];
}

async function getProfile(id: string) {
  candId.value = id;
  if (id === '0') {
    fullname.value = "Новая анкета";
    attr.value = 'alert-info';
    text.value = 'Заполните форму'
  } else {
    const response = await axios.get(`http://localhost:5000/profile/${id}`, {
    headers: {Authorization: `Bearer ${localStorage.getItem("jwt_token")}`}
    });
    const [anketa, check, registry, poligraf, investigation, inquiry, state] = response.data;
    questionary.value = anketa_labels.map((labels: string[], i: number) => `
      <div>${createItemTable(labels, anketa[i])}</div>
    `);
    fullname.value = anketa[0][0]['fullname'];
    status.value = anketa[0][0]['status'];
    condition.value = state;
    resume.value = anketa[0][0];
    lastCheck.value = check[0];
    verification.value = createItemTable(check_labels, check);
    register.value = createItemTable(registry_labels, registry);
    pfo.value = createItemTable(poligraf_labels, poligraf);
    inquisition.value = createItemTable(investigation_labels, investigation);
    needs.value = createItemTable(inquiry_labels, inquiry)
  }
}

function createItemTable(names: string[], response: Array<Array<Object>>) {
  if (!response.length) {
    return `<p>Данные отсутствуют</p>`
  }
  const rows = response.map((item) => {
    return names.map((name, i) => {
      if (Object.keys(item)[i] === 'deadline' || Object.keys(item)[i] === 'birthday') {
        const date = new Date(String(Object.values(item)[i]));
        return `<tr><td width="25%">${name}</td><td>${date.toLocaleDateString('ru-RU')}</td></tr>`;
      } else if (Object.keys(item)[i] === 'id' ) {
        return `<tr height="50px"><th colspan="2">${name} #${Object.values(item)[i]}</th></tr>`;
      } else if (Object.keys(item)[i] === 'path' ) {
        return `<tr><td width="25%">${name}</td><td><a href="${Object.values(item)[i]}">Открыть</a></td></tr>`;
      } else {
        return `<tr><td width="25%">${name}</td><td>${Object.values(item)[i]}</td></tr>`;
      }
    }).join('');
  });
  const body = `<tbody>${rows.join('')}</tbody>`;
  return `<table class="table table-responsive">${body}</table>`
}

</script>
