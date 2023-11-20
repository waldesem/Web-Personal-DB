<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { defineAsyncComponent } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';
import { identityStore } from '@store/identity';

const NavBar = defineAsyncComponent(() => import('@components/layouts/NavBar.vue'));
const AlertMessage = defineAsyncComponent(() => import('@components/layouts/AlertMessage.vue'));
const FooterDiv = defineAsyncComponent(() => import('@components/layouts/FooterDiv.vue'));
const ChatButton = defineAsyncComponent(() => import('@components/layouts/ChatButton.vue'));

const storeLogin = loginStore();
const storeIdentity = identityStore();

const route = useRoute();

watch(() => route.params.group,
  newValue => {
    storeIdentity.pageIdentity = newValue as string
  }, { immediate: true });


onBeforeMount(() => {
  storeLogin.userData.getAuth()
});

</script>


<template>
  <NavBar />
  <AlertMessage />
  <router-view></router-view>
  <ChatButton />
  <FooterDiv />
</template>
