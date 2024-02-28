<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { authStore } from "@store/auth"

const NavBar = defineAsyncComponent(
  () => import("@components/pages/admin/components/layouts/NavBar.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/pages/admin/components/layouts/AlertMessage.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/pages/admin/components/layouts/FooterDiv.vue")
);

const storeAuth = authStore();
</script>

<template>
  <NavBar 
    :full-name="storeAuth.userData.fullName"
    :user-logout="storeAuth.userData.userLogout"
  />
  <AlertMessage />
  <router-view v-slot="{ Component }">
    <transition name="component-fade" mode="out-in">
      <component :is="Component" :key="$route.fullPath" />
    </transition>
  </router-view>
  <FooterDiv 
    :has-admin="storeAuth.userData.hasAdmin"
  />
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
