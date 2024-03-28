<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  select: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});
</script>

<template>
  <select
    class="form-select"
    :id="props.name"
    :name="props.name"
    v-model="model"
  >
    <option v-for="value, key in props.select"
      :key="key"
      :value="value"
    >
      {{ value }}
    </option>
  </select>
</template>
