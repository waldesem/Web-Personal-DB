<script setup lang="ts">
import { stateClassify, userToken } from "@/state/state";

const classifyState = stateClassify();

await useAsyncData("candidates", async () => {
  if (!userToken.value) {
    return navigateTo("/login");
  }
  classifyState.getClassify();
  return navigateTo("/persons");
});
</script>

<template>
  <UProgress animation="swing" />
</template>
