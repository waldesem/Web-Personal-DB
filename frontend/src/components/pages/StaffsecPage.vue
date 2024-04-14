<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const NavBar = defineAsyncComponent(
  () => import("@components/content/layouts/NavBar.vue")
);
const MenuBar = defineAsyncComponent(
  () => import("@components/content/layouts/MenuBar.vue")
);
</script>

<template>
  <div class="container-fluid row px-3">
    <div class="col-2">
      <NavBar />
    </div>
    <div class="col-9">
      <MenuBar />
      <RouterView />
    </div>
    <div class="col-1"></div>
  </div>
</template>
