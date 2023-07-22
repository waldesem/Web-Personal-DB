<script setup lang="ts">

import { onBeforeMount } from 'vue';
import axios from 'axios';
import router from '@/router';
import config from '@/config';

onBeforeMount(async () => {
  try {
    const response = await axios.get(`${config.appUrl}/auth`, {
      headers: {Authorization: `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { access_token } = response.data;
    localStorage.setItem('jwt_token', access_token);
    access_token 
    ? router.push({ name: 'index', params: {flag: 'new'} }) 
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
