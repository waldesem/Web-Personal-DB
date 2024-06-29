<script setup lang="ts">
import { onMounted } from "vue";
import { router } from "@/router";

onMounted( () => {
  if (localStorage.getItem("user_token")) {
    router.push({ name: "staffsec" })
  } else {
    router.push({ name: "login" })
  }
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
