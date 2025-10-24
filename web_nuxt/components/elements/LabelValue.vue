<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  value: {
    type: [String, Number],
    default: "",
  },
});
</script>

<template>
  <div class="flex grid grid-cols-12 gap-3 mb-4">
    <div v-if="props.label" class="col-span-3">{{ props.label }}</div>
    <div v-else-if="$slots.label" class="col-span-3"><slot name="label" /></div>
    
    <div v-if="props.value" class="col-span-3 break-words">{{ props.value }}</div>
    <div v-else-if="$slots.value" class="col-span-9"><slot name="value" /></div>
  </div>
</template>
