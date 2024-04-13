<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);
const FooterDiv = defineAsyncComponent(
  () => import("@components/content/layouts/FooterDiv.vue")
);
</script>

<template>
  <NavBar />
  <div class="container-fluid row px-3">
    <div class="col-3">
      <MenuBar />
    </div>
    <div class="col-9">
      <router-view v-slot="{ Component }">
        <transition name="component-fade" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </transition>
      </router-view>
    </div>
  </div>
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
