<script setup lang="ts">
const props = defineProps({
  error: {
    type: Object as () => Record<string, unknown>,
    required: true,
  },
});
</script>

<template>
  <div class="text-center p-8 flex flex-col items-center h-screen">
    <h1 class="text-5xl font-bold text-red-800 mb-4">
      {{ props.error.statusCode }}
    </h1>
    <div class="text-primary my-4">
      <div class="text-2xl">{{ props.error.message }}</div>
      <div class="text-xl">{{ props.error.stack }}</div>
    </div>
    <NuxtLink to="/persons">Вернуться на главную страницу</NuxtLink>
  </div>
</template>
