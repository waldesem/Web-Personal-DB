<script setup lang="ts">
const model = defineModel();
const emit = defineEmits(["submit-data"]);
const props = defineProps({
  name: String,
  select: {
    type: Array,
    default: []
  },
});
</script>

<template>
  <select
    @change="emit('submit-data')"
    class="form-select"
    :id="props.name"
    :name="props.name"
    v-model.lazy="model"
  >
    <option v-for="value, idx in props.select"
      :key="idx"
      :value="value"
    >
      {{ value }}
    </option>
  </select>
</template>
