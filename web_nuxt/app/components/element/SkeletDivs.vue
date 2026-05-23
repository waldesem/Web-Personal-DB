<script setup lang="ts">
const props = defineProps({
  rows: {
    type: Number,
    required: true,
  },
});
</script>

<template>
  <div
    v-for="row in props.rows"
    :key="row"
    class="flex grid grid-cols-12 gap-3 mb-4"
  >
    <USkeleton class="col-span-3 h-6 w-full" />
    <USkeleton class="col-span-9 h-6 w-md" />
  </div>
</template>
