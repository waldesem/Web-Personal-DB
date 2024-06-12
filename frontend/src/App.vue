<script setup lang="ts">
import { onMounted } from "vue";
import { router } from "@/router";

onMounted( () => {
  router.push({ name: "persons" });
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
