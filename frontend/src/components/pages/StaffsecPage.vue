<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);
</script>

<template>
  <MenuBar />
  <div class="container-fluid row px-3">
    <div class="col-2">
      <NavBar />
    </div>
    <div class="col-10">
      <RouterView />
    </div>
  </div>
</template>