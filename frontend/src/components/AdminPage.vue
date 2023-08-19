<script setup lang="ts">
// Родительский компонент админки

import { onBeforeMount } from 'vue'
import { appAlert } from '@/store/alert';
import { appAuth } from '@store/auth';
import server from '@store/server';
import router from '@router/router';
import NavbarAdmin from '@layouts/NavbarAdmin.vue';
import AlertMessage from '@components/layouts/AlertMessage.vue';

const storeAuth = appAuth();

const storeAlert = appAlert();


// Проверка доступа к странице админки 
onBeforeMount(async () => {
  const response = await storeAuth.axiosInstance.get(`${server}/admin`);
  const { admin } = response.data;
  admin 
  ? router.push({ name: 'main', params: { flag: 'main'} }) 
  : router.push({ name: 'login' })
})

</script>

<template>
  <NavbarAdmin />
  <AlertMessage v-if="storeAlert.alertAttr && storeAlert.alertText" />
  <router-view v-slot="{ Component }" >
        <component :is="Component" :key="$route.fullPath"/>
    </router-view>
</template>
