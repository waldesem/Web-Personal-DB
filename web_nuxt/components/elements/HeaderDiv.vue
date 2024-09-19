<script setup lang="ts">
const props = defineProps({
  div: {
    type: String,
    default: "py-1",
  },
  cls: {
    type: String,
    default: "text-2xl text-red-800",
  },
  header: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div :class="props.div">
    <h3 class="font-bold" :class="props.cls">
      {{ props.header }}
    </h3>
  </div>
</template>
