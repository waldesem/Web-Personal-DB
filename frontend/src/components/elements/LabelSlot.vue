<script setup lang="ts">
const props = defineProps({
  divClass: {
    type: String,
    default: "row mb-3",
  },
  labelDivClass: {
    type: String,
    default: "col-md-3",
  },
  divSlotClass: {
    type: String,
    default: "col-md-9",
  },
  label: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div 
    :class="props.divClass">
    <div 
      :class="props.labelDivClass"
    >
      {{ props.label }}
    </div>
    <div 
      :class="props.divSlotClass"
    >
      <slot></slot>
    </div>
  </div>
</template>
