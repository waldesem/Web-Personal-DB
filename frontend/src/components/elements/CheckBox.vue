<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  divClass: {
    type: String,
    default: "offset-lg-2 col-lg-10",
  },
  divInput: {
    type: String,
    default: "form-check form-switch",
  },
  input: {
    type: String,
    default: "form-check-input",
  },
  typeof: {
    type: String,
    default: "checkbox",
  },
  role: {
    type: String,
    default: "switch",
  },
  id: String,
  label: String,
})
</script>
<template>
  <div class="row">
    <div :class="props.divClass">
      <div :class="props.divInput">
        <input
          :class="props.input"
          :type="props.typeof"
          :role="props.role"
          :id="props.id"
          :name="props.id"
          v-model="model"
        />
        <label class="form-check-label" :for="props.id">
          {{ props.label }}
        </label>
      </div>
    </div>
  </div>
  </template>