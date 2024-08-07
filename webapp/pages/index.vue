<script setup lang="ts">
import { onBeforeMount } from "vue";
import  { stateUser } from "@/utils/state";

onBeforeMount(async () => {
  const user = stateUser();
  await user.getCurrentUser();
});
</script>

<template>
  <div></div>
</template>
