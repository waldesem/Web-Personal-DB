<script setup lang="ts">
useHead({ htmlAttrs: { lang: "ru" } });
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
