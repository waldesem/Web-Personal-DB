<script setup lang="ts">
await navigateTo("/persons");
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" :height="5" />
    <NuxtLayout>
      <NuxtPage :transition="true" />
    </NuxtLayout>
  </UApp>
</template>
