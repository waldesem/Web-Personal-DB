<script setup lang="ts">
const props = defineProps({
  label: {
    type: String,
    default: "",
  },
  labelClass: {
    type: String,
    default: "col-lg-3",
  },
  inputClass: {
    type: String,
    default: "col-lg-9",
  }
});
</script>

<template>
  <div class="row mb-3">
    <div :class="props.labelClass">
      {{ props.label }}
    </div>
    <div :class="props.inputClass">
      <slot></slot>
    </div>
  </div>
</template>


<style scoped>
@media print {
  .col-lg-2, .col-lg-10 {
    float: left!important;
  }
  .col-lg-10 {
    width: 70%;
  }
  .col-lg-2 {
    width: 30%;
  }
}
</style>