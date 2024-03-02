<script setup lang="ts">
import { onBeforeMount } from "vue";
import { classifyStore } from "./store/classify";
import { userStore } from "./store/user";

const storeClasses = classifyStore();
const storeUser = userStore();

onBeforeMount(async () => {
  await storeUser.userData.getAuth();
  await storeClasses.classData.getClasses();
});
</script>

<template>
  <RouterView />
</template>

<style>
html,
body {
  scrollbar-gutter: stable;
}
</style>
