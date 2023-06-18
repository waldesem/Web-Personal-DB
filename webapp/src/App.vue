<template>
  <router-view ></router-view>
</template>

<script setup lang="ts">

import axios from 'axios';
import router from './router';

(async (): Promise<void> => {
  const token = localStorage.getItem('jwt_token');
  if (!token) {
    router.push({ name: 'login' });
  }
  try {
    const response = await axios.get('http://localhost:5000/login', {
      headers: {'Authorization': `Bearer ${token}`}
    });
    const { user } = response.data;
    user === "Authorized" 
      ? router.push({ name: 'index', params: { flag: 'new' } }) 
      : router.push({ name: 'login' });
  } catch {
    router.push({ name: 'login' })
  }
})();
  
</script>
