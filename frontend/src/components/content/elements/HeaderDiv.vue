<script setup lang="ts">
const props = defineProps({
  pageHeader: String,
  cls: {
    type: String,
    default: "text-info py-3",
  },
});
</script>

<template>
  <div class="text-opacity-85" :class="cls">
    <h3>{{ props.pageHeader }}</h3>
  </div>
</template>
