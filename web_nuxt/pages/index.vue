<script setup lang="ts">
import  { stateUser } from "@/state/state";

const user = stateUser();
await user.getCurrentUser();
</script>

<template>
  <UProgress animation="swing" />
</template>