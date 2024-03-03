<script setup lang="ts">
const props = defineProps({
  need: {
    type: Boolean,
    default: false,
  },
  pattern: {
    type: String,
    default: ".*",
  },
  place: String,
  name: String,
  model: {
    type: [String, Number],
    default: "",
  },
  lst: String,
  selects: Array,
});
</script>

<template>
  <div class="mb-3 row">
    <div class="col-lg-11">
      <input
        class="form-control"
        max="255"
        type="text"
        :id="props.name"
        :name="props.name"
        :required="props.need"
        :pattern="props.pattern"
        :placeholder="props.place"
        :list="props.lst"
        :value="props.model"
        @input="$emit('input-event', $event)"
      />
      <datalist v-if="props.lst" :id="props.lst">
        <option v-for="item in selects" :value="item"></option>
      </datalist>
    </div>
  </div>
</template>
