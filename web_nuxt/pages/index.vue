<script setup lang="ts">
import { stateUser, stateClassify } from "@/state/state";

const userState = stateUser();
const classifyState = stateClassify();

Promise.all([userState.getCurrentUser(), classifyState.getClassify()]);
</script>

<template>
  <UProgress animation="swing" />
</template>
