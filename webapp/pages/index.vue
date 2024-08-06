<script setup lang="ts">
import { onBeforeMount } from "vue";
import { stateUser } from "@/utils/state";

onBeforeMount(async () => {
  await stateUser.getCurrentUser();
});
</script>

<template>
  <NuxtLoadingIndicator />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
