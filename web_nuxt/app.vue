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

<style>
html,
body {
  scrollbar-gutter: stable;
}

/* body {
  margin-right: 20px;
} */

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
