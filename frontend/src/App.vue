<script setup lang="ts">
import { onBeforeMount } from "vue";
import { authStore } from "@/store/auth";

const storeAuth = authStore();

onBeforeMount(async () => {
  await storeAuth.userData.getAuth();
});
</script>

<template>
  <router-view></router-view>
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}
</style>
