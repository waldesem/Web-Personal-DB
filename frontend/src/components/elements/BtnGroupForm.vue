<script setup lang="ts">

const props = defineProps({
  disable: {
    type: Boolean,
    default: false
  }
});

</script>

<template>
  <div class="row" :disabled="props.disable">
    <div class="offset-lg-2 col-lg-10">
      <div class="btn-group" role="group">
        <slot></slot>
      </div>
    </div>
  </div>
</template>