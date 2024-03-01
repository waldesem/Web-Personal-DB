<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const AlertMessage = defineAsyncComponent(
  () => import("@components/layouts/AlertMessage.vue")
);
const NavBar = defineAsyncComponent(
  () => import("@components/content/admin/layouts/NavBar.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/content/admin/layouts/FooterDiv.vue")
);
</script>

<template>
  <NavBar />
  <AlertMessage />
  <router-view v-slot="{ Component }">
    <transition name="component-fade" mode="out-in">
      <component :is="Component" :key="$route.fullPath" />
    </transition>
  </router-view>
  <FooterDiv />
</template>

<style scoped>
.component-fade-enter-active,
.component-fade-leave-active {
  transition: opacity 0.2s ease-in-out;
}
.component-fade-enter,
.component-fade-leave-to {
  opacity: 0;
}
</style>
