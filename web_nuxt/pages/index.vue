<script setup lang="ts">
definePageMeta({ layout: false });

await navigateTo("/persons");
</script>

<template>
  <div class="flex flex-col justify-center">
    <LazyUProgress animation="swing" />
  </div>
</template>
