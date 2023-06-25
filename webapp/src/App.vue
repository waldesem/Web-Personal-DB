<template>
  <router-view ></router-view>
</template>

<script setup lang="ts">

import { onBeforeMount } from 'vue';
import axios from 'axios';
import router from '@/router';
import appUrl from '@/config';

onBeforeMount(async () => {
  const token = localStorage.getItem('jwt_token');
  if (!token) {
    router.push({ name: 'login' });
    return
  } 
  try {
    const response = await axios.get(`${appUrl}/auth`, {
      headers: {'Authorization': `Bearer ${token}`}
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
