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
  <div class="row mb-3">
    <div class="col-md-3">
      {{ props.label }}
    </div>
    <div class="col-md-9">
      {{ props.value }}
    </div>
  </div>
</template>
