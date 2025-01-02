<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div class="flex grid grid-cols-12 gap-3 mb-3">
    <div class="col-span-3">
      {{ props.label }}
    </div>
    <div class="col-span-6 break-words">
      <slot />
    </div>
  </div>
</template>
