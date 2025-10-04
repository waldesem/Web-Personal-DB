<script setup lang="ts">
definePageMeta({
  middleware: (from) => {
    if (from.path === "/") {
      return navigateTo("/persons");
    }
  },
});
</script>

<template>
  <div><!-- Пустая страница --></div>
</template>
