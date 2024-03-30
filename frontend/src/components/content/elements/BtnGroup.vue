<script setup lang="ts">
const props = defineProps({
  disable: {
    type: Boolean,
    default: false,
  },
  offset: {
    type: Boolean,
    default: true
  }
});
</script>

<template>
  <div class="row mb-3" :disabled="props.disable">
    <div :class="{'offset-lg-3 col-lg-9' : props.offset}">
      <div class="btn-group" role="group">
        <slot></slot>
      </div>
    </div>
  </div>
</template>
