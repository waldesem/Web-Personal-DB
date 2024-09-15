<script setup lang="ts">
import { stateClassify, userToken } from "@/state/state";

const classifyState = stateClassify();

await useAsyncData("candidates", async () => {
  if (!userToken.value) {
    return navigateTo("/login");
  }
  Promise.all([classifyState.getClassify(), navigateTo("/persons")]);
});
</script>

<template>
  <UProgress animation="swing" />
</template>
