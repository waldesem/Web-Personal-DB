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
    class="flex grid grid-cols-12 gap-3 mb-3"
  >
    <div class="col-span-3">
      <USkeleton class="h-4" />
    </div>
    <div class="col-span-9">
      <USkeleton class="h-4 w-[300px]" />
    </div>
  </div>
</template>
