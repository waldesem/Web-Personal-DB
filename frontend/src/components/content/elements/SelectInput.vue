<script setup lang="ts">
const model = defineModel();
const emit = defineEmits(["submit-data"]);
const props = defineProps({
  name: String,
  select: {
    type: [Array, Object],
    default: function() {
      return {};
    },
    validator: function(value) {
      return Array.isArray(value) || typeof value === 'object';
    },
  },
});
</script>

<template>
  <select
    @change="emit('submit-data')"
    class="form-select"
    :id="props.name"
    :name="props.name"
    v-model="model"
  >
    <option v-for="value, keydex in props.select"
      :key="keydex"
      :value="keydex"
    >
      {{ value }}
    </option>
  </select>
</template>
