<script setup lang="ts">
import { userToken } from "@/utils/auth";

await useAsyncData("candidates", async () => {
  if (!userToken.value) {
    return navigateTo("/login");
  }
  return navigateTo("/persons");
});
</script>

<template><div>Index</div></template>
