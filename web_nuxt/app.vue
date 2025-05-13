<script setup lang="ts">
useHead({
  htmlAttrs: { lang: "ru" },
  title: "StaffSec - кадровая безопасность",
  meta: [
    { name: "description", content: "Кадровая безопасность" },
    { name: "viewport", content: "width=device-width, initial-scale=1" },
  ],
  link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
});

preloadRouteComponents("/persons");

await navigateTo("/persons");
</script>

<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage :transition="true" />
    </NuxtLayout>
  </UApp>
</template>
