<script setup lang="ts">
const props = defineProps({
  rows: {
    type: Number,
    default: 3,
  },
});
</script>

<template>
  <UCard>
  <div
    v-for="i in props.rows"
    :key="i"
    class="flex grid grid-cols-6 gap-3 mb-3"
  >
    <div class="col-span-1">
      <USkeleton class="h-4" />
    </div>
    <div class="col-span-5">
      <USkeleton class="h-4 w-[300px]" />
    </div>
  </div>
  </UCard>
</template>
