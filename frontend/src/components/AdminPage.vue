<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import server from '@store/server';
import router from '../router/router';
import { appAuth } from '../store/auth';
import NavbarAdmin from './admin/NavbarAdmin.vue';
import AlertMessage from './AlertMessage.vue';

const storeAuth = appAuth()

const data = ref({
  attr: '',
  text: ''
})


onBeforeMount(async () => {
  const response = await storeAuth.axiosInstance.get(`${server}/admin`);
  const { admin } = response.data;
  admin 
  ? router.push({ name: 'main', params: { flag: 'main'} }) 
  : router.push({ name: 'login' })
})


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