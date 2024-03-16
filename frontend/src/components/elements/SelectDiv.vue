<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  isneed: {
    type: Boolean,
    default: true,
  },
  name: String,
  label: String,
  select: {
    type: Object as () => Record<string, any>,
    default: () => [],
  },
  selectValue: String,
  selectName: String,
});
</script>

<template>
  <div class="mb-3 row">
    <label class="col-form-label col-lg-2" :for="props.name">
      {{ props.label }}
    </label>
    <div class="col-lg-10">
      <select
        class="form-select"
        :required="props.isneed"
        :id="props.name"
        :name="props.name"
        v-model="model"
      >
        <option
          v-for="(key, value) in props.select"
          :key="key"
          :value="value"
        >
          {{key }}
        </option>
      </select>
    </div>
  </div>
</template>
