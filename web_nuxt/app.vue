<script setup lang="ts">
await preloadRouteComponents("/persons");

await navigateTo("/persons");
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" />
    <NuxtLayout>
      <NuxtPage :transition="true" />
    </NuxtLayout>
  </UApp>
</template>
