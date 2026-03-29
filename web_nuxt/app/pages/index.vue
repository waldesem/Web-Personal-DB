<script setup lang="ts">
definePageMeta({
  layout: false,
  middleware: (from: { path: string }) => {
    if (from.path === "/") {
      return navigateTo("/persons");
    }
  },
});
</script>

<template>
  <UContainer>Index</UContainer>
</template>
