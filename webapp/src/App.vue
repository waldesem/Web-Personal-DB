<script setup lang="ts">

import { onBeforeMount } from 'vue';
import axios from 'axios';
import router from '@/router';
import config from '@/config';

onBeforeMount(async () => {
  try {
    const response = await axios.get(`${config.appUrl}/auth`, {
      headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`}
    });
    const { access } = response.data;
    access === "Authorized" 
    ? router.push({ name: 'index', params: {flag: 'new', page: 1} }) 
    : router.push({ name: 'login' });
  } catch (error) {
    console.error(error)
    router.push({ name: 'login' })
  }
});
  
</script>

<template>
  <router-view/>
</template>
