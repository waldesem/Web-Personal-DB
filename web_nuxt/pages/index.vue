<script setup lang="ts">
import { stateClassify } from "@/state/state";

const classifyState = stateClassify();

await useAsyncData("candidates", async () => {
  await classifyState.getClassify();
  await navigateTo("/persons");
})
</script>

<template>
  <UProgress animation="swing" />
</template>
