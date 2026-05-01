<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div class="flex grid grid-cols-12 gap-3 mb-4">
    <div class="col-span-3">
      {{ props.label }}
    </div>
    <div class="col-span-9">
      <slot />
    </div>
  </div>
</template>
