<script setup lang="ts">
import { router } from "@/router";
router.push({ name: "staffsec" })
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
