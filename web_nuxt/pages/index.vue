<script setup lang="ts">
import { userToken } from "@/state/state";

await useAsyncData("candidates", async () => {
  if (!userToken.value) {
    return navigateTo("/login");
  }
  return navigateTo("/persons");
});
</script>

<template>
  <UProgress animation="swing" />
</template>
