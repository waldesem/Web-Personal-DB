<script setup lang="ts">
const props = defineProps({
  rows: {
    type: Number,
    default: 3,
  },
});
</script>

<template>
  <ElementLabelValue v-for="row in props.rows" :key="row">
    <template #label>
      <USkeleton class="h-6" />
    </template>
    <USkeleton class="h-6 w-[300px]" />
  </ElementLabelValue>
</template>
