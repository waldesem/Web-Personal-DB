<script setup lang="ts">
import { stateClassify } from "@/state/state";

const classifyState = stateClassify();

await useAsyncData("candidates", async () => {
  Promise.all([classifyState.getClassify(), navigateTo("/persons")]);
});
</script>

<template>
  <UProgress animation="swing" />
</template>
