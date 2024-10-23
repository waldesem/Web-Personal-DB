<script setup lang="ts">
definePageMeta({
  layout: false,
});

preloadRouteComponents("/persons")
preloadRouteComponents("/login");

await navigateTo("/persons");
</script>

<template><div>Index</div></template>
