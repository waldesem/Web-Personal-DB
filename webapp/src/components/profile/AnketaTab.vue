<template>
  <ModalWin :candId="candId" :path="url"/>
  <div v-if="candId==='0'" class="py-3">
    <UploadFile @updateMessage="updateMessage" @updateItem="updateItem"/>
    <ResumeForm :resume="resume" @cancelEdit="cancelEdit" @updateMessage="updateMessage" @updateItem="updateItem"/>
  </div>
  <div v-else class="py-3">
    <h6>Резюме</h6>
    <div v-html="table ? table[0] : ''"></div>
    <button @click="url = 'staff'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
    <div v-html="table ? table[1] : ''"></div>
    <button @click="url = 'document'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
    <div v-html="table ? table[2] : ''"></div>
    <button @click="url = 'address'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
    <div v-html="table ? table[3] : ''"></div>
    <button @click="url = 'contact'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
    <div v-html="table ? table[4] : ''"></div>
    <button @click="url = 'workplace'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
    <div v-html="table ? table[5] : ''"></div>
    <div class="btn-group" role="group">
      <button @click="id='0'" class="btn btn-outline-primary">Изменить анкету</button>
      <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
      <button @click="sendResume" :disabled="state && (status !== state['NEWFAG'] && status !== state['UPDATE'])" class="btn btn-outline-primary">Отправить на проверку</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref, toRefs, defineProps, defineEmits, watch } from 'vue';
import ResumeForm from './ResumeForm.vue';
import UploadFile from './UploadFile.vue';
import ModalWin from './ModalWin.vue';

const props = defineProps({
  table: Array,
  candId: String,
  resume: Object,
  state: Object,
  status: String
});

const {table, candId, resume, state, status} = toRefs(props);

const emit = defineEmits(['updateMessage', 'updateItem']);

const url = ref('');
const id = ref('');

function updateMessage(data: Object) {
  emit('updateMessage', data)
}

function updateItem(data: Object) {
  id.value = String(data['candId' as keyof typeof data]);
  console.log(id.value)
  emit('updateItem', id.value);
}

function cancelEdit() {
  id.value = String(candId);
}

async function updateStatus() {
  const response = await axios.get(`http://localhost:5000/resume/status/${candId?.value}`, {
    headers : {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  emit('updateMessage', {
    attr: "alert-info",
    text: message
  });
  window.scrollTo(0,0)
}

async function sendResume() {
  const response = await axios.get(`http://localhost:5000/resume/send/${candId?.value}`, {
    headers : {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  emit('updateMessage', {
    attr: "alert-info",
    text: message
  });
  window.scrollTo(0,0)
}

watch(
  () => id.value,
  (newId) => {
    updateItem({candId: newId});
  }
);
</script>
