<script setup lang="ts">

import { onMounted } from 'vue';
import { appLogin } from '@/store/login';
import { appAlert } from '@/store/alert';
import FooterDiv from '@layouts/FooterDiv.vue';
import AlertMessage from '@layouts/AlertMessage.vue';

const storeLogin = appLogin();
const storeAlert = appAlert();

onMounted(() => {
  storeLogin.getAuth()
});
  
</script>

<template>
<NavBar />
  <AlertMessage v-if="storeAlert.alertAttr && storeAlert.alertText" />
  <router-view v-slot="{ Component }" >
    <transition name="component-fade" mode="out-in">
      <component :is="Component" :key="$route.fullPath"/>
    </transition>
  </router-view>
  <FooterDiv />
</template>

<style scoped>

.component-fade-enter-active, .component-fade-leave-active {
  transition: opacity .1s ease;
}
.component-fade-enter, .component-fade-leave-to {
  opacity: 0;
}
</style>