<script setup lang="ts">
const model = defineModel();
const props = defineProps(["name"]);
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
    />
  </div>
</template>