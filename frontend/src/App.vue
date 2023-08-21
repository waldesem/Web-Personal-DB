<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { appLogin } from '@/store/login';
import FooterDiv from '@layouts/FooterDiv.vue';

const storeLogin = appLogin();

// Запрос авторизации пользователя перед запуском приложения
onBeforeMount(async () => {
  storeLogin.getAuth()
});
  
</script>

<template>
  <router-view/>
  <FooterDiv />
</template>
