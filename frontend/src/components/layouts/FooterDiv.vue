<script setup lang="ts">
// Компонент для отображения подвала

import server from '@store/server';
import { appLogin } from '@/store/login';

const loginStore = appLogin();

const doc_url = `${server}/docs`;

</script>

<template>
  <div class="container py-5">
    <footer class="d-flex flex-wrap justify-content-around align-items-center py-3 my-4 border-top">
      <p><router-link :to="{ name: 'persons' }">Home</router-link></p>
      <p><a :href="doc_url" target=”_blank”>OpenAPI</a></p>
      <p v-if="loginStore.userRole === 'admin'"><router-link :to="{ name: 'admin' }">Admin</router-link></p>
      <p><a href="https://github.com/waldesem/Web-Personal-DB">GitHub</a></p>
    </footer>
  </div>
</template>