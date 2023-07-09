<template>
  <router-view ></router-view>
</template>

<script setup lang="ts">

import { onBeforeMount } from 'vue';
import axios from 'axios';
import router from '@/router';
import config from '@/config';

onBeforeMount(async () => {
  try {
    const response = await axios.get(`${config.appUrl}/auth`, {
      headers: {'Authorization': `Bearer ${config.token}`}
    });
    const { user } = response.data;
    user === "Authorized" 
    ? router.push({ name: 'index', params: { flag: 'new' } }) 
    : router.push({ name: 'login' });
  } catch {
    router.push({ name: 'login' })
  }
});
  
</script>
