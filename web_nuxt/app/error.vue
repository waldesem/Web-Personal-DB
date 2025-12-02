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
      statusCode: props.error.statusCode,
      statusMessage: props.error.statusMessage,
      message: props.error.message,
    }"
  />
</template>
