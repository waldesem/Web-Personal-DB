<script setup lang="ts">
const model = defineModel<string>();
const props = defineProps({
  name: String,
  place: String,
});
</script>

<template>
  <textarea
    class="form-control"
    :id="props.name"
    :name="props.name"
    :placeholder="props.place"
    v-model.lazy="model"
  >
  </textarea>
</template>
