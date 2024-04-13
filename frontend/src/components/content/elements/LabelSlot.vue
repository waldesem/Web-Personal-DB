<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  noPrint: {
    type: Boolean,
    default: false,
  },
  labelClass: {
    type: String,
    default: "col-lg-2",
  },
  inputClass: {
    type: String,
    default: "col-lg-10",
  }
});
</script>

<template>
  <div class="row mb-3" :class="{ 'd-print-none': props.noPrint }">
    <div :class="props.labelClass">
      {{ props.label }}
    </div>
    <div :class="props.inputClass">
      <slot></slot>
    </div>
  </div>
</template>
