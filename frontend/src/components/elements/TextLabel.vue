<script setup lang="ts">
const model = defineModel<string>();
const props = defineProps({
  name: String,
  label: String,
});
</script>

<template>
  <div class="mb-3 row">
    <label class="col-form-label col-lg-2" :for="props.name">
      {{ props.label }}
    </label>
    <div class="col-lg-10">
      <textarea
        class="form-control"
        :id="props.name"
        :name="props.name"
        :placeholder="props.label"
        v-model="model"
      >
      </textarea>
    </div>
  </div>
</template>
