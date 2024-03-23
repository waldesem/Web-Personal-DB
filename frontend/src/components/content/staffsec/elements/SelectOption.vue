<script setup lang="ts">
const model = defineModel();
const emit = defineEmits(["submit-data"]);
const props = defineProps({
  class: String,
  name: String,
  selected: String,
  select: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});
</script>

<template>
  <div :class="props.class">
    <select
      @change="emit('submit-data')"
      class="form-select"
      :id="props.name"
      :name="props.name"
      v-model="model"
    >
      <option 
        :value="props.selected" 
        selected
      >
        {{ props.selected }}
      </option>
      <option
        v-for="(value, key) in props.select"
        :key="key"
        :value="key"
      >
        {{ value }}
      </option>
    </select>
  </div>
</template>
