<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';

const NavBar = () => import('@components/layouts/NavBar.vue');
const AlertMessage = () => import('@components/layouts/AlertMessage.vue');
const FooterDiv = () => import('@components/layouts/FooterDiv.vue');
const ChatButton = () => import('@components/layouts/ChatButton.vue');

const storeLogin = loginStore();
const route = useRoute();

onBeforeMount(() => {
  storeLogin.getAuth()
});

watch(() => route.params.group,
  newValue => {
    storeLogin.pageIdentity = newValue as string;
  }
);

</script>

<template>
  <NavBar />
  <AlertMessage />
  <router-view></router-view>
  <chat-button />
  <FooterDiv />
</template>
