<script setup lang="ts">
preloadRouteComponents("/persons");

await navigateTo("/persons");
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <KeepAlive include="persons">
        <NuxtPage :transition="true" />
      </KeepAlive>
    </NuxtLayout>
  </UApp>
</template>
