<script setup lang="ts">
definePageMeta({ layout: false });

preloadRouteComponents("/persons");

await navigateTo("/persons");
</script>

<template><div>Index</div></template>
