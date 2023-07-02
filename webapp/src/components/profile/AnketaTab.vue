<template>
  <ModalWin :candId="candId" :path="urlId.url" @updateItem="updateItem"/>
  <div v-if="urlId.id==='0'" class="py-3">
    <UploadFile @updateMessage="updateMessage" @updateItem="updateItem"/>
    <ResumeForm :resume="resume" @cancelEdit="cancelEdit" @updateMessage="updateMessage" @updateItem="updateItem"/>
  </div>
  <div v-else class="py-3">
    <h6>Резюме</h6>
    <div v-html="table ? table[0] : ''"></div>
    <button @click="urlId.url = 'staff'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
    <div v-html="table ? table[1] : ''"></div>
    <button @click="urlId.url = 'document'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
    <div v-html="table ? table[2] : ''"></div>
    <button @click="urlId.url = 'address'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
    <div v-html="table ? table[3] : ''"></div>
    <button @click="urlId.url = 'contact'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
    <div v-html="table ? table[4] : ''"></div>
    <button @click="urlId.url = 'workplace'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
    <div v-html="table ? table[5] : ''"></div>
    <div class="btn-group" role="group">
      <button @click="updateItem({candId: '0'})" class="btn btn-outline-primary">Изменить анкету</button>
      <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
      <button @click="sendResume('send')" :disabled="state && (status !== state['NEWFAG'] && status !== state['UPDATE'])" class="btn btn-outline-primary">Отправить на проверку</button>
      <button @click="sendResume('check')" disabled class="btn btn-outline-primary">Начать проверку</button>
    </div>
  </div>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import ResumeForm from './ResumeForm.vue';
import UploadFile from './UploadFile.vue';
import ModalWin from './ModalWin.vue';
import appUrl from '@/config';
import router from '@/router';

const props = defineProps({
  table: Array,
  candId: String,
  resume: Object,
  state: Object,
  status: String
});
const {table, candId, resume, state, status} = toRefs(props);

const emit = defineEmits(['updateMessage', 'updateItem']);

const urlId = ref({
  url: '',
  id: candId?.value
});

function updateMessage(data: Object) {
  emit('updateMessage', data)
}

function updateItem(data: Object) {
  urlId.value.id = String(data['candId' as keyof typeof data]);
  emit('updateItem', urlId.value.id);
}

function cancelEdit() {
  String(candId?.value) !== '0' 
  ? urlId.value.id = String(candId) 
  : router.push({ name: 'index', params: { flag: 'new' } })
}

async function updateStatus() {
  const response = await axios.get(`${appUrl}/resume/status/${status?.value}/${candId?.value}`, {
    headers : {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  emit('updateMessage', {
    attr: "alert-info",
    text: message
  });
  window.scrollTo(0,0)
}

async function sendResume(flag: string) {
  const response = await axios.get(`${appUrl}/resume/${flag}/${candId?.value}`, {
    headers : {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  emit('updateMessage', {
    attr: "alert-info",
    text: message
  });
  window.scrollTo(0,0)
}

</script>
