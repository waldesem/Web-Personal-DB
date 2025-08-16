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
  <div><!-- Index --></div>
</template>
