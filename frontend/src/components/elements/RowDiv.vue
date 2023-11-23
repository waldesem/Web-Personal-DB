<script setup lang="ts">

const props = defineProps({
  label: String,
  value: String
});
  
</script>

<template>
  <div class="row">
    <div class="col-md-4">{{props.label}}</div>
    <div class="col-md-8">{{props.value}}</div>
  </div>
</template>