<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  print: {
    type: Boolean,
    default: true,
  },
});
</script>

<template>
  <div class="row mb-3" :class="{ 'd-print-none': props.print }">
    <div class="col-md-3">
      {{ props.label }}
    </div>
    <div class="col-md-9">
      <slot></slot>
    </div>
  </div>
</template>
