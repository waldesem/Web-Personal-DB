<script setup lang="ts">
import type { NuxtError } from "#app";

const props = defineProps({
  error: {
    type: Object as () => NuxtError,
    required: true,
  },
});
</script>

<template>
  <div class="text-center p-8 flex flex-col items-center h-screen">
    <h1 class="text-5xl font-bold text-red-800 mb-4">
      {{ props.error.statusCode }}
    </h1>
    <p class="text-red-800 mb-4">{{ props.error.message }}</p>
    <p class="text-red-800 mb-4">{{ props.error.stack }}</p>
    <NuxtLink to="/">Go back home</NuxtLink>
  </div>
</template>
