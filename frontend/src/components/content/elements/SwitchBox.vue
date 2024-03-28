<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  divClass: {
    type: String,
    default: "form-check form-switch mb-3",
  },
  inputClass: {
    type: String,
    default: "form-check-input",
  },
  labelClass: {
    type: String,
    default: "form-check-label",
  },
  typeof: {
    type: String,
    default: "checkbox",
  },
  role: {
    type: String,
    default: "switch",
  },
  name: String,
  label: String,
})
</script>
<template>
  <div :class="props.divClass">
    <input
      :class="props.inputClass"
      :type="props.typeof"
      :role="props.role"
      :id="props.name"
      :name="props.name"
      v-model="model"
    />
    <label 
      :class="props.labelClass" 
      :for="props.name"
    >
      {{ props.label }}
    </label>
  </div>
  </template>