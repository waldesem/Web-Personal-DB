<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  labelClass: {
    type: String,
    default: "col-span-1",
  },
  inputClass: {
    type: String,
    default: "col-span-5 break-words",
  }
});
</script>

<template>
  <div class="flex grid grid-cols-6 gap-3 mb-3 text-sm text-gray-500 dark:text-gray-400">
    <div :class="props.labelClass">
      {{ props.label }}
    </div>
    <div :class="props.inputClass">
      <slot/>
    </div>
  </div>
</template>
