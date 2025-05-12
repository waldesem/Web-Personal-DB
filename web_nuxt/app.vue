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

<style>
/* html,
body {
  scrollbar-gutter: stable;
} */

body {
  padding-right: 9px;
  margin-right: 0px;
  scrollbar-width: 9px;
  overflow: hidden;
  pointer-events: none;
}

.page-enter-active,
.page-leave-active,
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.1s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
