<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  title: String,
  place: String,
  lst: String,
  need: {
    type: Boolean,
    default: false,
  },
  selects: Array,
});
</script>

<template>
  <div class="mb-3 row">
    <input
      class="form-control"
      max="255"
      type="text"
      :id="props.title"
      :name="props.title"
      :required="props.need"
      :placeholder="props.place"
      :list="props.lst"
      v-model.trim="model"
    />
    <datalist v-if="props.lst" :id="props.lst">
      <option v-for="item in selects" :value="item"></option>
    </datalist>
  </div>
</template>
