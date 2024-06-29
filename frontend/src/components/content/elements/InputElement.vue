<script setup lang="ts">
const emit = defineEmits(["submit-data"]);
const model = defineModel();
const props = defineProps({
  name: String,
  place: String,
  lst: {
    type: String,
    default: ""
  },
  selects: {
    type: Array,
    default: []
  },
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
    autocomplete="new-password username"
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
    :list="props.lst"
    v-model.trim.lazy="model"
    @change="emit('submit-data')"
  />
  <datalist v-if="props.lst" :id="props.lst">
    <option v-for="item in selects" 
      :value="item">
    </option>
  </datalist>
</template>
