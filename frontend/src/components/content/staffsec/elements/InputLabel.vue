<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  name: String,
  label: String,
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
  <div class="mb-3 row">
    <label class="col-form-label col-lg-2" :for="props.name">
      {{ props.label }}
    </label>
    <div class="col-lg-10">
      <input
        class="form-control"
        :id="props.name"
        :name="props.name"
        :type="props.typeof"
        :max="props.max"
        :required="props.need"
        :pattern="props.pattern"
        :placeholder="props.label"
        :list="props.lst"
        v-model.trim="model"
      />
      <datalist v-if="props.lst" :id="props.lst">
        <option v-for="item in selects" 
          :value="item">
        </option>
    </datalist>
    </div>
  </div>
</template>
