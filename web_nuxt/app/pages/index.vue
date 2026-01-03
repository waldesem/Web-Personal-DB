<script setup lang="ts">
definePageMeta({
  layout: false,
  middleware: (from) => {
    if (from.path === "/") {
      return navigateTo("/persons");
    }
  },
});
</script>

<template>
  <UContainer>Index</UContainer>
</template>
