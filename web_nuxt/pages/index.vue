<script setup lang="ts">
definePageMeta({
  layout: false,
});

preloadRouteComponents("/persons")
preloadRouteComponents("/login");

await useAsyncData("index", async () => {
  if (!userToken.value) {
    return navigateTo("/login");
  }
  return navigateTo("/persons");
});
</script>

<template><div>Index</div></template>
