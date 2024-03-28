<script setup lang="ts">
const model = defineModel();
const props = defineProps(["name"]);
const emit = defineEmits(["submit-data"]);
</script>

<template>
  <div class="col-md-2">
    <input
      class="form-control"
      :id="props.name"
      :name="props.name"
      required
      type="date"
      v-model="model"
      @change="emit('submit-data')"
    />
  </div>
</template>