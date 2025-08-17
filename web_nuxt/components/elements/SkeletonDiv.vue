<script setup lang="ts">
// Компонент для отображения скилета для элементов
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
      <USkeleton class="h-6" />
    </div>
    <div class="col-span-9">
      <USkeleton class="h-6 w-[300px]" />
    </div>
  </div>
</template>
