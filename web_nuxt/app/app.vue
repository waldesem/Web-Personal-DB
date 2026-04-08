<script setup lang="ts">
useHead({ htmlAttrs: { lang: "ru" } });
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" :height="3" />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
