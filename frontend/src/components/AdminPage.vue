<script setup lang="ts">
// Родительский компонент админки

import { onBeforeMount, ref } from 'vue'
import server from '@store/server';
import router from '@router/router';
import { appAuth } from '@store/auth';
import NavbarAdmin from '@layouts/NavbarAdmin.vue';
import AlertMessage from '@components/layouts/AlertMessage.vue';

const storeAuth = appAuth()

// Аттрибут и текст сообщения на странице админки
const data = ref({
  attr: '',
  text: ''
})

// Проверка доступа к странице админки 
onBeforeMount(async () => {
  const response = await storeAuth.axiosInstance.get(`${server}/admin`);
  const { admin } = response.data;
  admin 
  ? router.push({ name: 'main', params: { flag: 'main'} }) 
  : router.push({ name: 'login' })
})

// Обновление сообщения на странице админки
function updateMessage(alert: Object){
  data.value.attr = (alert as { attr: string })["attr"];
  data.value.text = (alert as { text: string })["text"];
}

</script>

<template>
  <NavbarAdmin />
  <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
  <router-view @updateMessage="updateMessage" />
</template>