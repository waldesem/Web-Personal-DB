<script setup lang="ts">
preloadRouteComponents("/persons");

await navigateTo("/persons");
</script>

<template>
  <UApp :scroll-body="{ margin: 20 }">
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <NuxtPage :transition="true" />
    </NuxtLayout>
  </UApp>
</template>
