<script setup lang="ts">
import { onBeforeMount } from "vue";
import  { stateUser } from "@/state/state";

onBeforeMount(async () => {
  const user = stateUser();
  await user.getCurrentUser();
});
</script>

<template>
  <div/>
</template>
