<script setup lang="ts">
const props = defineProps({
  label: String,
});
</script>

<template>
  <div class="row mb-3">
    <div class="col-md-3">
      {{ props.label }}
    </div>
    <div class="col-md-9">
      <slot></slot>
    </div>
  </div>
</template>
