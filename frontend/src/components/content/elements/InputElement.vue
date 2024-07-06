<script setup lang="ts">
const emit = defineEmits(["submit-data"]);
const model = defineModel();
const props = defineProps({
  name: String,
  place: String,
  typeof: {
    type: String,
    default: "text",
  },
  need: {
    type: Boolean,
    default: false,
  },
  disable: {
    type: Boolean,
    default: false,
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
    :minlength="props.min"
    :maxlength="props.max"
    :required="props.need"
    :disabled="props.disable"
    :pattern="props.pattern"
    :placeholder="props.place"
    v-model.trim.lazy="model"
    @change="emit('submit-data')"
  />
</template>
