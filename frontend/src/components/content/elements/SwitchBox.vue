<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  label: String,
})
</script>
<template>
  <div class="form-check form-switch mb-3">
    <input
      class="form-check-input"
      type="checkbox"
      role="switch"
      :id="props.name"
      :name="props.name"
      v-model="model"
    />
    <label 
      class="form-check-label" 
      :for="props.name"
    >
      {{ props.label }}
    </label>
  </div>
  </template>