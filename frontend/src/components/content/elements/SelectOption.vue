<script setup lang="ts">
const model = defineModel();
const emit = defineEmits(["submit-data"]);
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
    @change="emit('submit-data')"
    class="form-select"
    :id="props.name"
    :name="props.name"
    v-model="model"
  >
    <option
      v-for="(value, key) in props.select"
      :key="key"
      :value="key"
    >
      {{ value }}
    </option>
  </select>
</template>
