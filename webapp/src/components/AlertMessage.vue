<template>
  <div class="alert alert-dismissible" :class="props.attr" role="info">{{props.text}}
    <button class="btn-close" type="button" data-bs-dismiss="alert"></button>
  </div>
</template>

<script setup lang="ts">

const props = defineProps({
  attr: String,
  text: String
});

</script>