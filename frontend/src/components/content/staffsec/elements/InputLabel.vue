<script setup lang="ts">
const model = defineModel();
const props = defineProps({
  need: {
    type: Boolean,
    default: false,
  },  
  name: String,
  label: String,
  typeof: {
    type: String,
    default: "text",
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
    default: "",
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
        v-model.trim="model"
      />
    </div>
  </div>
</template>
