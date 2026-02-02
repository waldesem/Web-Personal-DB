<script setup lang="ts">
import type { NuxtError } from "nuxt/app";

const props = defineProps({
  error: {
    type: Object as () => NuxtError,
    required: true,
  },
});
</script>

<template>
  <UError
    :clear="{
      color: 'neutral',
      size: 'xl',
      icon: 'i-lucide-arrow-left',
      class: 'rounded-full',
    }"
    :error="{
      statusCode: props.error.status,
      statusMessage: props.error.message,
      message: props.error.message,
    }"
  />
</template>
