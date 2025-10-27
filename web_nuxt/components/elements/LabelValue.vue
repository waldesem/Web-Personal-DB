<script setup lang="ts">
const props = defineProps({
  divClass: {
    type: String,
    default: "flex grid grid-cols-12 gap-3 mb-4",
  },
  label: {
    type: String,
    default: "",
  },
  value: {
    type: [String, Number],
    default: "",
  },
  labelClass: {
    type: String,
    default: "col-span-3",
  },
  valueClass: {
    type: String,
    default: "col-span-9",
  },
});
</script>

<template>
  <div v-if="props.value || $slots.value" :class="props.labelClass">
    <div v-if="props.label" :class="props.labelClass">{{ props.label }}</div>
    <div v-else-if="$slots.label" :class="props.labelClass">
      <slot name="label" />
    </div>

    <div v-if="props.value" :class="props.valueClass" class="break-words">
      {{ props.value }}
    </div>
    <div v-else-if="$slots.value" :class="props.valueClass">
      <slot />
    </div>
  </div>
</template>
