<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { loginStore } from '@/store/login';
import { defineAsyncComponent } from 'vue';
import { useRoute } from 'vue-router';

const NavBar = defineAsyncComponent(() => import('@components/layouts/NavBar.vue'));
const AlertMessage = defineAsyncComponent(() => import('@components/layouts/AlertMessage.vue'));
const FooterDiv = defineAsyncComponent(() => import('@components/layouts/FooterDiv.vue'));
const ChatButton = defineAsyncComponent(() => import('@components/layouts/ChatButton.vue'));

const route = useRoute();

const storeLogin = loginStore();

watch(() => route.params.group,
  newValue => {
    storeLogin.pageIdentity = newValue as string
  }, { immediate: true });


onBeforeMount(() => {
  storeLogin.getAuth()
});

</script>


<template>
  <NavBar />
  <AlertMessage />
  <router-view></router-view>
  <ChatButton />
  <FooterDiv />
</template>
