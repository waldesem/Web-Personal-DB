<script setup lang="ts">

import { onBeforeMount } from 'vue'
import axios from 'axios';
import config from '../config';
import router from '../router';


onBeforeMount(async () => {
  const response = await axios.get(`${config.appUrl}/admin`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  });
  const { admin } = response.data;
  admin 
  ? router.push({ name: 'main', params: { flag: 'main', page: 1 } }) 
  : router.push({ name: 'login' })
})

</script>

<template></template>../router/router