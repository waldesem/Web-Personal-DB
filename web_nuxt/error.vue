<script setup lang="ts">
import type { NuxtError } from 'nuxt/app';

const props = defineProps({
  error: {
    type: Object as () => NuxtError,
    required: true,
  },
});
</script>

<template>
  <div class="flex flex-col items-center h-screen p-8">
    <h1 class="text-4xl font-bold text-red-800 mb-4">
      {{ props.error.name }}
    </h1>
    <div class="text-primary my-4">
      <div class="text-2xl">{{ props.error.message }}</div>
      <div class="text-xl">{{ props.error.stack }}</div>
    </div>
    <UButton label="Очистить ошибку" @click="clearError({ redirect: '/'})"/>
  </div>
</template>
