<script setup lang="ts">
const props = defineProps({
  label: String,
  noPrint: {
    type: Boolean,
    default: false,
  }
});
</script>

<template>
  <div class="row mb-3" :class="{ 'd-print-none': props.noPrint }">
    <div class="col-md-3">
      {{ props.label }}
    </div>
    <div class="col-md-9">
      <slot></slot>
    </div>
  </div>
</template>
