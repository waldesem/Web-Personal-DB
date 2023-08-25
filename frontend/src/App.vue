<script setup lang="ts">

import { onMounted } from 'vue';
import { appLogin } from '@/store/login';
import FooterDiv from '@layouts/FooterDiv.vue';

const storeLogin = appLogin();

onMounted(() => {
  storeLogin.getAuth()
});
  
</script>

<template>
  <router-view/>
  <FooterDiv />
</template>
