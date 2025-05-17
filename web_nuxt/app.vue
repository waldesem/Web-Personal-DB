<script setup lang="ts">
preloadRouteComponents("/persons");

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
