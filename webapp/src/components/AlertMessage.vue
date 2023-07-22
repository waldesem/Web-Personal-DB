<template>
  <div class="alert alert-dismissible" :class="props.attr" role="info">{{props.text}}</div>
</template>

<script setup lang="ts">

const props = defineProps({
  attr: String,
  text: String
});

</script>