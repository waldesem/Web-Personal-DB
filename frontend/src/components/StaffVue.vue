<script setup lang="ts">

import { onMounted } from 'vue';
import { appAlert } from '@/store/alert';
import router from '@router/router';
import NavBar from '@layouts/NavBar.vue'
import AlertMessage from '@layouts/AlertMessage.vue';

const storeAlert = appAlert();

onMounted(() => {
  router.push({ name: 'persons' }) // Переход на страницу с кандидатами
})

</script>

<template>
  <NavBar />
  <AlertMessage v-if="storeAlert.alertAttr && storeAlert.alertText" />
  <router-view v-slot="{ Component }" >
    <transition name="component-fade" mode="out-in">
      <component :is="Component" :key="$route.fullPath"/>
    </transition>
  </router-view>
</template>

<style scoped>

.component-fade-enter-active, .component-fade-leave-active {
  transition: opacity .1s ease;
}
.component-fade-enter, .component-fade-leave-to {
  opacity: 0;
}
</style>