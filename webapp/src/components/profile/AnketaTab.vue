<template>
  <ModalWin :candId="candId" :path="data.flag" @updateItem="updateItem"/>
  <div class="py-3">
    <template v-if="data.id==='0'" >
      <UploadFile @updateMessage="updateMessage" @updateItem="updateItem"/>
      <ResumeForm :resume="resume" @cancelEdit="cancelEdit" @updateMessage="updateMessage" @updateItem="updateItem"/>
    </template>
    <template v-else >
      <h6>Резюме</h6>
      <div v-html="table ? table[0] : ''"></div>
      <button @click="data.flag = 'staff'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
      <div v-html="table ? table[1] : ''"></div>
      <button @click="data.flag = 'document'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
      <div v-html="table ? table[2] : ''"></div>
      <button @click="data.flag = 'address'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
      <div v-html="table ? table[3] : ''"></div>
      <button @click="data.flag = 'contact'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
      <div v-html="table ? table[4] : ''"></div>
      <button @click="data.flag = 'workplace'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
      <div v-html="table ? table[5] : ''"></div>
      <div class="btn-group" role="group">
        <button @click="updateItem('0')" class="btn btn-outline-primary">Изменить анкету</button>
        <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
        <button @click="sendResume" :disabled="config.status && (status !== config.status['newfag'] && status !== config.status['update'])" 
          class="btn btn-outline-primary">Отправить на проверку</button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import ResumeForm from './ResumeForm.vue';
import UploadFile from './UploadFile.vue';
import ModalWin from './ModalWin.vue';
import config from '@/config';
import router from '@/router';

const props = defineProps({
  table: Array,
  candId: String,
  resume: Object,
  status: String
});

const emit = defineEmits(['updateMessage', 'updateItem']);

const data = ref({flag: ''});

function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};

function updateItem(resp_id: string) {
  emit('updateItem', resp_id);
};

function cancelEdit() {
  props.candId !== '0' 
  ? updateItem(props.candId)
  : router.push({ name: 'index', params: { flag: 'new' } })
};

async function updateStatus() {
  const response = await axios.get(`${config.appUrl}/resume/status/${props.candId}`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  updateMessage({
    attr: message == 'update' ? "alert-success" : "alert-warning",
    text: message == 'update' ? "Статус обновлен" : "Анкету с текущим статусом обновить нельзя",
  });
  window.scrollTo(0,0)
}

async function sendResume() {
  const response = await axios.get(`${config.appUrl}/resume/send/${props.candId}`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  const textMessage = {
    robot: ['Анкета кандидата взята в работу', "alert-success"],
    error: ['Отправка анкеты кандидата не удалась. Попробуйте позднее', "alert-info"],
    cancel: ['Анкета не может быть отправлена. Проверка уже начата', "alert-danger"]
  };
  updateMessage({
    attr: textMessage[message as keyof typeof textMessage][1],
    text: textMessage[message as keyof typeof textMessage][0]
  });
  window.scrollTo(0,0)
}

</script>
