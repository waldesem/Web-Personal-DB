<script setup lang="ts">
useHead({
  htmlAttrs: { lang: "ru" },
  link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  meta: [
    { name: "description", content: "Кадровая безопасность" },
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { charset: "utf-8" },
  ],
});
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" :height="3" />
    <NuxtLayout> <NuxtPage :transition="{ name: 'page' }" /> </NuxtLayout>
  </UApp>
</template>
