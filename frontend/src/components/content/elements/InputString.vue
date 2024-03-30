<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  place: String,
  lst: {
    type: String,
    default: ""
  },
  selects: {
    type: Array,
    default: []
  },
  typeof: {
    type: String,
    default: "text",
  },
  need: {
    type: Boolean,
    default: false,
  },  
  max: {
    type: [String, Number],
    default: (props: any) => {
      if (props.typeof === "date") {
        return new Date().toISOString().split("T")[0];
      } else {
        return "255";
      }
    },
  },
  pattern: {
    type: String,
    default: ".*",
  },
});
</script>

<template>
  <input
    class="form-control"
    :id="props.name"
    :name="props.name"
    :type="props.typeof"
    :max="props.max"
    :required="props.need"
    :pattern="props.pattern"
    :placeholder="props.place"
    :list="props.lst"
    v-model.trim="model"
  />
  <datalist v-if="props.lst" :id="props.lst">
    <option v-for="item in selects" 
      :value="item">
    </option>
  </datalist>
</template>
