<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  label: String,
  title: {
    type: String,
    default: "",
  }
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
      :title="props.label"
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