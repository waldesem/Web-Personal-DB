<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  place: String,
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
    default: "524288",
  },
  pattern: {
    type: String,
    default: ".*",
  }
});
</script>

<template>
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
      :placeholder="props.place"
      :pattern="props.pattern"
      v-model="model"
    />
    <slot></slot>
  </div>
</template>