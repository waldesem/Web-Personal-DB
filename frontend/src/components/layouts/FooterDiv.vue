<script setup lang="ts">
// Компонент для отображения подвала

import server from '@store/server';
import { appLogin } from '@/store/login';
import { appProfile } from '@/store/profile';

const loginStore = appLogin();
const profileStore = appProfile();

const doc_url = `${server}/docs`;

</script>

<template>
  <div v-if="!profileStore.printPdf" class="container py-5">
    <footer class="d-flex flex-wrap justify-content-around align-items-center py-3 my-4 border-top">
      <p><router-link :to="{ name: 'persons' }">Home</router-link></p>
      <p><a :href="doc_url" target=”_blank”>OpenAPI</a></p>
      <p v-if="loginStore.hasRole('admin')"><router-link :to="{ name: 'admin' }">Admin</router-link></p>
      <p><a href="https://github.com/waldesem/StaffSec">GitHub</a></p>
    </footer>
  </div>
</template>