<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  labelClass: {
    type: String,
    default: "text-md",
  },
  inputClass: {
    type: String,
    default: "text-md break-words",
  }
});
</script>

<template>
  <div class="row columns-2 mb-3">
    <div :class="props.labelClass">
      {{ props.label }}
    </div>
    <div :class="props.inputClass">
      <slot/>
    </div>
  </div>
</template>
