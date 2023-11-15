<script setup lang="ts">

const props = defineProps({
  pageHeader: String
});

</script>

<template>
  <div class="text-primary text-opacity-85 py-5">
    <h3>{{ props.pageHeader }}</h3>
  </div>
</template>