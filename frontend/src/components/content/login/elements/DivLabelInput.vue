<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  label: String,
  type: {
    type: String,
    default: "text",
  },
  min: {
    type: [String, Number],
    default: "",
  },
  max: {
    type: [String, Number],
    default: "",
  },
  pattern: {
    type: String,
    default: "",
  }
});
</script>

<template>
  <div class="mb-3 row">
    <label 
      class="col-form-label col-lg-2" 
      :for="props.name"
    >
      {{ props.label }}
    </label>
    <div class="col-lg-8">
      <div class="input-group">
        <input
          :autocomplete="props.name"
          class="form-control"
          required
          :id="props.name"
          :name="props.name"
          :type="props.type"
          :minlength="props.min"
          :maxlength="props.max"
          :placeholder="props.label"
          :pattern="props.pattern"
          v-model="model"
        />
          <slot></slot>
        </div>
    </div>
  </div>
</template>