<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';
import NavBar from '@components/layouts/NavBar.vue';
import AlertMessage from '@components/layouts/AlertMessage.vue';
import FooterDiv from '@components/layouts/FooterDiv.vue';
import ChatButton from '@components/layouts/ChatButton.vue';

const route = useRoute();

const storeLogin = loginStore();

watch(() => route.params.group,
  newValue => {
    storeLogin.pageIdentity = newValue as string
  }, {immediate: true});
  
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
