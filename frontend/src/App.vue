<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { appLogin } from '@/store/login';
import FooterDiv from '@layouts/FooterDiv.vue';
import AlertMessage from '@layouts/AlertMessage.vue';
import NavBar from '@layouts/NavBar.vue';

const storeLogin = appLogin();
const route = useRoute();

watch(() => route.params.group,
  newValue => {
    storeLogin.pageIdentity = newValue as string;
  }
);

onBeforeMount(() => {
  storeLogin.getAuth()
});

</script>

<template>
  <NavBar />
  <AlertMessage />
  <router-view></router-view>
  <FooterDiv />
</template>
