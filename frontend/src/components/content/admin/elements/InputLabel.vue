<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  need: {
    type: Boolean,
    default: true,
  },  
  name: String,
  label: String,
  typeof: {
    type: String,
    default: "text",
  },
  min: {
    type: [String, Number],
    default: "3",
  },
  max: {
    type: [String, Number],
    default: "255"
  },
  pattern: {
    type: String,
    default: ".*",
  },
});
</script>

<template>
  <input
    class="form-control"
    :id="props.name"
    :name="props.name"
    :type="props.typeof"
    :min="props.min"
    :max="props.max"
    :required="props.need"
    :pattern="props.pattern"
    :placeholder="props.label"
    v-model.trim="model"
  />
</template>
