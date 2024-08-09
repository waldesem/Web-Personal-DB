<script setup lang="ts">
const props = defineProps({
  pageHeader: {
    type: String,
    default: "",
  },
  cls: {
    type: String,
    default: "py-5",
  },
  clsHead: {
    type: String,
    default: "text-red-600",
  },
});
</script>

<template>
  <div :class="props.cls">
    <h3 class="text-2xl text-opacity-75 font-bold" :class="props.clsHead">
      {{ props.pageHeader }}
    </h3>
  </div>
</template>
