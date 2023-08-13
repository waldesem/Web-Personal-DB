<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { appAuth } from '@store/auth';
import { locationStore } from '@store/location';
import { appClassify } from '@store/classify';
import router from '@router/router';
import server from '@store/server';
import FooterDiv from '@layouts/FooterDiv.vue';


const storeAuth = appAuth()

const storeLocation = locationStore();

const classifyApp = appClassify();

// Запрос авторизации пользователя перед запуском приложения
onBeforeMount(async () => {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/auth`);
    const { access } = response.data;
    
    access === "Authorized" 
    ? router.push({ name: 'persons' })
    : router.push({ name: 'login' });
    
    storeLocation.getRegions();  // Получение списка регионов
    classifyApp.getClassify();  // Получение списка категорий
  
  } catch (error) {
    console.error(error)
    router.push({ name: 'login' })
  }
});
  
</script>

<template>
  <router-view/>
  <FooterDiv />
</template>
